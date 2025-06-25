"""
Vertex AI KFP Pipeline for Development
- Preprocesses data from GCS.
- Trains a model.
- Evaluates the model.
- Conditionally proceeds based on accuracy.
"""
from kfp.v2 import dsl # Keep this import for dsl.Condition
from kfp.v2.dsl import component, pipeline, Input, Output, Dataset, Model, Metrics

PIPELINE_NAME = "mlops-diabetes-dev-pipeline"
PIPELINE_DESCRIPTION = "Development pipeline for diabetes prediction model on Vertex AI"

GCS_PACKAGE_REQUIREMENTS = [
    "google-cloud-storage==2.10.0",
    "pandas==1.5.3",
    "scikit-learn==1.2.2", # Match version from SageMaker if possible, or update
    "joblib==1.2.0"
]

@component(
    base_image="python:3.9",
    packages_to_install=GCS_PACKAGE_REQUIREMENTS,
)
def preprocess_data_op(
    input_gcs_uri: str,  # GCS URI to the raw diabetes.csv
    output_train_data: Output[Dataset],
    output_test_data: Output[Dataset]
):
    """Loads raw data, splits into train/test, and saves to GCS."""
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
    train_data: Input[Dataset], # Updated from InputPath("Dataset")
    output_model: Output[Model], # Updated from OutputPath("Model")
    reg_rate: float
):
    """Trains a logistic regression model and saves it."""
    import pandas as pd
    import joblib
    from sklearn.linear_model import LogisticRegression
    import logging
    import os

    logging.basicConfig(level=logging.INFO)

    train_df = pd.read_csv(train_data.path) # Access path via .path

    columns = ['Pregnancies', 'PlasmaGlucose', 'DiastolicBloodPressure',
               'TricepsThickness', 'SerumInsulin', 'BMI', 'DiabetesPedigree', 'Age']
    X_train = train_df[columns]
    y_train = train_df['Diabetic']

    model = LogisticRegression(C=1 / reg_rate, solver="liblinear")
    model.fit(X_train, y_train.values.ravel())

    joblib.dump(model, output_model.path) # Access path via .path
    logging.info(f"Model trained and saved to {output_model.path}") # Access path via .path

@component(
    base_image="python:3.9",
    packages_to_install=GCS_PACKAGE_REQUIREMENTS,
)
def evaluate_model_op(
    test_data: Input[Dataset], # Updated from InputPath("Dataset")
    model: Input[Model],       # Updated from InputPath("Model")
    metrics: Output[Metrics],  # Updated from OutputPath("Metrics")
    min_accuracy: float
) -> float: # Returns accuracy
    """Evaluates the model and returns accuracy."""
    import pandas as pd
    import joblib
    from sklearn.metrics import accuracy_score
    import json
    import logging
    import os

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
def model_approved_op(model_accuracy: float, model: Input[Model]):
    """Placeholder for actions after model approval."""
    import logging
    logging.basicConfig(level=logging.INFO)
    logging.info(f"Model at {model.uri} approved with accuracy: {model_accuracy}. Ready for registration/deployment.")

@component(
    base_image="python:3.9",
)
def model_rejected_op(model_accuracy: float, min_accuracy: float):
    """Placeholder for actions if model is rejected."""
    import logging
    logging.basicConfig(level=logging.INFO)
    # To fail the pipeline, raise an exception.
    raise ValueError(f"Model REJECTED. Accuracy {model_accuracy} is below threshold {min_accuracy}.")

@pipeline(
    name=PIPELINE_NAME,
    description=PIPELINE_DESCRIPTION
)
def dev_diabetes_pipeline(
    input_raw_data_gcs_uri: str, # e.g., gs://your-bucket/raw-data/diabetes.csv
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
        model_approved_op(
            model_accuracy=evaluate_task.outputs["accuracy"],
            model=train_task.outputs["output_model"]
        )
    with dsl.Condition(evaluate_task.outputs["accuracy"] < min_accuracy, name="accuracy-too-low"):
        model_rejected_op(
            model_accuracy=evaluate_task.outputs["accuracy"],
            min_accuracy=min_accuracy
        )