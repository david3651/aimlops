"""
Vertex AI KFP Pipeline for Development
- Preprocesses data from GCS.
- Trains a model.
- Evaluates the model.
- Conditionally proceeds based on accuracy.
- Registers the model in Vertex AI Model Registry if approved.
"""
from kfp.v2 import dsl  # Keep this import for dsl.Condition
from kfp.v2.dsl import component, pipeline, Input, Output, Dataset, Model, Metrics

PIPELINE_NAME = "mlops-diabetes-dev-pipeline"
PIPELINE_DESCRIPTION = "Development pipeline for diabetes prediction model on Vertex AI"

GCS_PACKAGE_REQUIREMENTS = [
    "google-cloud-storage==2.10.0",
    "pandas==1.5.3",
    "scikit-learn==1.2.2",  # Match version from SageMaker if possible, or update
    "joblib==1.2.0",
    "google-cloud-aiplatform==1.38.1"  # Added for Vertex AI Model Registry
]

@component(
    base_image="python:3.9",
    packages_to_install=GCS_PACKAGE_REQUIREMENTS,
)
def preprocess_data_op(
    input_gcs_uri: str,
    output_train_data: Output[Dataset],
    output_test_data: Output[Dataset]
):
    import pandas as pd
    from google.cloud import storage
    from urllib.parse import urlparse
    import logging
    import os

    logging.basicConfig(level=logging.INFO)
    parsed_uri = urlparse(input_gcs_uri)
    bucket_name = parsed_uri.netloc
    blob_name = parsed_uri.path.lstrip('/')

    local_raw_data_file = "diabetes_raw.csv"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.download_to_filename(local_raw_data_file)
    logging.info(f"Downloaded raw data from {input_gcs_uri} to {local_raw_data_file}")

    df = pd.read_csv(local_raw_data_file)
    train_data = df.sample(frac=0.8, random_state=42)
    test_data = df.drop(train_data.index)

    train_data.to_csv(output_train_data.path, index=False)
    test_data.to_csv(output_test_data.path, index=False)
    logging.info(f"Train data saved to {output_train_data.path}")
    logging.info(f"Test data saved to {output_test_data.path}")

@component(
    base_image="python:3.9",
    packages_to_install=GCS_PACKAGE_REQUIREMENTS,
)
def train_model_op(
    train_data: Input[Dataset],
    output_model: Output[Model],
    reg_rate: float
):
    import pandas as pd
    import joblib
    from sklearn.linear_model import LogisticRegression
    import logging

    logging.basicConfig(level=logging.INFO)
    train_df = pd.read_csv(train_data.path)
    columns = ['Pregnancies', 'PlasmaGlucose', 'DiastolicBloodPressure',
               'TricepsThickness', 'SerumInsulin', 'BMI', 'DiabetesPedigree', 'Age']
    X_train = train_df[columns]
    y_train = train_df['Diabetic']

    model = LogisticRegression(C=1 / reg_rate, solver="liblinear")
    model.fit(X_train, y_train.values.ravel())
    joblib.dump(model, output_model.path)
    logging.info(f"Model trained and saved to {output_model.path}")

@component(
    base_image="python:3.9",
    packages_to_install=GCS_PACKAGE_REQUIREMENTS,
)
def evaluate_model_op(
    test_data: Input[Dataset],
    model: Input[Model],
    metrics: Output[Metrics],
    min_accuracy: float
) -> float:
    import pandas as pd
    import joblib
    from sklearn.metrics import accuracy_score
    import logging

    logging.basicConfig(level=logging.INFO)
    model_artifact = joblib.load(model.path)
    test_df = pd.read_csv(test_data.path)
    columns = ['Pregnancies', 'PlasmaGlucose', 'DiastolicBloodPressure',
               'TricepsThickness', 'SerumInsulin', 'BMI', 'DiabetesPedigree', 'Age']
    X_test = test_df[columns]
    y_test = test_df['Diabetic']

    y_pred = model_artifact.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    metrics.log_metric("accuracy", accuracy)
    metrics.log_metric("min_accuracy_threshold", min_accuracy)
    logging.info(f"Model accuracy: {accuracy}")
    logging.info(f"Evaluation metrics saved to {metrics.path}")
    return accuracy

@component(
    base_image="python:3.9",
)
def model_approved_op():
    """Dummy component to signify model approval."""
    import logging
    logging.basicConfig(level=logging.INFO)
    logging.info("Model accuracy meets the threshold. Proceeding with registration.")

@component(
    base_image="python:3.9",
    packages_to_install=GCS_PACKAGE_REQUIREMENTS,
)
def register_model_op(
    project_id: str,
    region: str,
    model_display_name: str,
    model_artifact: Input[Model],
    registered_model: Output[Model]
):
    """Uploads the model to Vertex AI Model Registry."""
    from google.cloud import aiplatform
    import logging

    logging.basicConfig(level=logging.INFO)
    aiplatform.init(project=project_id, location=region)
    logging.info(f"Registering model '{model_display_name}' from {model_artifact.uri}")

    artifact_dir = model_artifact.uri.rsplit('/', 1)[0]
    model = aiplatform.Model.upload(
        display_name=model_display_name,
        artifact_uri=artifact_dir,
        serving_container_image_uri="us-docker.pkg.dev/vertex-ai/prediction/sklearn-cpu.1-2:latest",
        sync=True
    )
    registered_model.uri = model.resource_name
    logging.info(f"Model registered: {model.resource_name}")

@component(
    base_image="python:3.9",
)
def model_rejected_op(model_accuracy: float, min_accuracy: float):
    import logging
    logging.basicConfig(level=logging.INFO)
    raise ValueError(f"Model REJECTED. Accuracy {model_accuracy} is below threshold {min_accuracy}.")

@pipeline(
    name=PIPELINE_NAME,
    description=PIPELINE_DESCRIPTION
)
def dev_diabetes_pipeline(
    project_id: str,
    region: str,
    model_display_name: str,
    input_raw_data_gcs_uri: str,
    reg_rate: float = 0.05,
    min_accuracy: float = 0.70
):
    preprocess_task = preprocess_data_op(
        input_gcs_uri=input_raw_data_gcs_uri
    )

    train_task = train_model_op(
        train_data=preprocess_task.outputs["output_train_data"],
        reg_rate=reg_rate
    )

    evaluate_task = evaluate_model_op(
        model=train_task.outputs["output_model"],
        test_data=preprocess_task.outputs["output_test_data"],
        min_accuracy=min_accuracy
    )

    with dsl.Condition(evaluate_task.outputs["accuracy"] >= min_accuracy, name="accuracy-check"):
        model_approved_op_task = model_approved_op()
        register_task = register_model_op(
            project_id=project_id,
            region=region,
            model_display_name=model_display_name,
            model_artifact=train_task.outputs["output_model"]
        ).after(model_approved_op_task)

    with dsl.Condition(evaluate_task.outputs["accuracy"] < min_accuracy, name="accuracy-too-low"):
        model_rejected_op(
            model_accuracy=evaluate_task.outputs["accuracy"],
            min_accuracy=min_accuracy
        )
