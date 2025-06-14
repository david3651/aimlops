"""
Vertex AI KFP Pipeline for Production
- Preprocesses data from GCS.
- Trains a model.
- Evaluates the model.
- Conditionally proceeds based on accuracy for production.
"""

from kfp import dsl
from kfp.dsl import OutputPath, InputPath

PIPELINE_NAME = "mlops-diabetes-prod-pipeline"
PIPELINE_DESCRIPTION = "Production pipeline for diabetes prediction model on Vertex AI"

GCS_PACKAGE_REQUIREMENTS = [
    "google-cloud-storage==2.10.0",
    "pandas==1.5.3",
    "scikit-learn==1.2.2", # Match version from SageMaker if possible, or update
    "joblib==1.2.0"
]

# Re-using component definitions from dev or define them identically.
# For a real-world scenario, you might import these from a shared components library.

@dsl.component(
    base_image="python:3.9",
    packages_to_install=GCS_PACKAGE_REQUIREMENTS,
)
def preprocess_data_op(
    input_gcs_uri: str,
    output_train_path: OutputPath("Dataset"),
    output_test_path: OutputPath("Dataset")
):
    """Loads raw data, splits into train/test, and saves to GCS."""
    import pandas as pd
    from google.cloud import storage
    from urllib.parse import urlparse
    import logging
    import os

    logging.basicConfig(level=logging.INFO)
    logging.info(f"[PROD] Preprocessing data from {input_gcs_uri}")

    parsed_uri = urlparse(input_gcs_uri)
    bucket_name = parsed_uri.netloc
    blob_name = parsed_uri.path.lstrip('/')

    local_raw_data_file = "diabetes_raw_prod.csv"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.download_to_filename(local_raw_data_file)
    logging.info(f"[PROD] Downloaded raw data from {input_gcs_uri} to {local_raw_data_file}")

    df = pd.read_csv(local_raw_data_file)

    train_data = df.sample(frac=0.8, random_state=42) # Consistent split
    test_data = df.drop(train_data.index)

    train_data.to_csv(output_train_path, index=False)
    test_data.to_csv(output_test_path, index=False)
    logging.info(f"[PROD] Train data saved to {output_train_path}")
    logging.info(f"[PROD] Test data saved to {output_test_path}")


@dsl.component(
    base_image="python:3.9",
    packages_to_install=GCS_PACKAGE_REQUIREMENTS,
)
def train_model_op(
    train_data_path: InputPath("Dataset"),
    output_model_path: OutputPath("Model"),
    reg_rate: float
):
    """Trains a logistic regression model and saves it."""
    import pandas as pd
    import joblib
    from sklearn.linear_model import LogisticRegression
    import logging
    import os

    logging.basicConfig(level=logging.INFO)
    logging.info(f"[PROD] Training model with reg_rate: {reg_rate}")

    train_data = pd.read_csv(train_data_path)

    columns = ['Pregnancies', 'PlasmaGlucose', 'DiastolicBloodPressure',
               'TricepsThickness', 'SerumInsulin', 'BMI', 'DiabetesPedigree', 'Age']
    X_train = train_data[columns]
    y_train = train_data['Diabetic']

    model = LogisticRegression(C=1 / reg_rate, solver="liblinear")
    model.fit(X_train, y_train)

    joblib.dump(model, output_model_path)
    logging.info(f"[PROD] Model trained and saved to {output_model_path}")


@dsl.component(
    base_image="python:3.9",
    packages_to_install=GCS_PACKAGE_REQUIREMENTS,
)
def evaluate_model_op(
    model_path: InputPath("Model"),
    test_data_path: InputPath("Dataset"),
    metrics_path: OutputPath("Metrics")
) -> float: # Returns accuracy
    """Evaluates the model and returns accuracy."""
    import pandas as pd
    import joblib
    from sklearn.metrics import accuracy_score
    import json
    import logging
    import os

    logging.basicConfig(level=logging.INFO)
    logging.info(f"[PROD] Evaluating model from {model_path}")

    model = joblib.load(model_path)
    test_data = pd.read_csv(test_data_path)

    columns = ['Pregnancies', 'PlasmaGlucose', 'DiastolicBloodPressure',
               'TricepsThickness', 'SerumInsulin', 'BMI', 'DiabetesPedigree', 'Age']
    X_test = test_data[columns]
    y_test = test_data['Diabetic']

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    metrics_data = {"accuracy": accuracy}
    with open(metrics_path, "w") as f:
        json.dump(metrics_data, f)

    logging.info(f"[PROD] Model accuracy: {accuracy}")
    logging.info(f"[PROD] Evaluation metrics saved to {metrics_path}")
    return accuracy

@dsl.component(
    base_image="python:3.9",
)
def model_approved_op(model_accuracy: float, model_path: InputPath("Model")):
    import logging
    logging.basicConfig(level=logging.INFO)
    logging.info(f"[PROD] Model at {model_path} approved with accuracy: {model_accuracy}. Ready for production deployment processes.")

@dsl.component(
    base_image="python:3.9",
)
def model_rejected_op(model_accuracy: float, min_accuracy: float):
    import logging
    logging.basicConfig(level=logging.INFO)
    logging.error(f"[PROD] Model REJECTED. Accuracy {model_accuracy} is below threshold {min_accuracy}. Halting production deployment.")
    # Consider raising an exception to fail the pipeline explicitly
    # import sys
    # sys.exit(1)

@dsl.pipeline(
    name=PIPELINE_NAME,
    description=PIPELINE_DESCRIPTION
)
def prod_diabetes_pipeline(
    input_raw_data_gcs_uri: str, # e.g., gs://your-prod-bucket/raw-data/diabetes.csv
    output_gcs_base_path: str,   # e.g., gs://your-prod-bucket/pipeline-outputs/prod/
    reg_rate: float = 0.05,      # Consistent with SageMaker prod
    min_accuracy: float = 0.80   # From SageMaker prod pipeline
):
    preprocess_task = preprocess_data_op(
        input_gcs_uri=input_raw_data_gcs_uri
    )

    train_task = train_model_op(
        train_data_path=preprocess_task.outputs["output_train_path"],
        reg_rate=reg_rate
    )

    evaluate_task = evaluate_model_op(
        model_path=train_task.outputs["output_model_path"],
        test_data_path=preprocess_task.outputs["output_test_path"]
    )

    with dsl.Condition(evaluate_task.output >= min_accuracy, name="prod-accuracy-check"):
        model_approved_op(
            model_accuracy=evaluate_task.output,
            model_path=train_task.outputs["output_model_path"]
        )
    with dsl.Condition(evaluate_task.output < min_accuracy, name="prod-accuracy-too-low"):
        model_rejected_op(
            model_accuracy=evaluate_task.output,
            min_accuracy=min_accuracy
        )