"""
Evaluation script for SageMaker ProcessingStep.
Evaluates the trained model and logs accuracy metrics.
"""

import argparse
import pandas as pd
import joblib
from sklearn.metrics import accuracy_score
import json
import os

def evaluate_model(model_path, test_data_path, output_metrics_path):
    print("Loading test dataset...")
    test_data = pd.read_csv(test_data_path)

    columns = ['Pregnancies', 'PlasmaGlucose', 'DiastolicBloodPressure',
               'TricepsThickness', 'SerumInsulin', 'BMI', 'DiabetesPedigree', 'Age']
    X_test = test_data[columns]
    y_test = test_data['Diabetic']

    model = joblib.load(model_path)
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    metrics = {"accuracy": accuracy}
    os.makedirs(os.path.dirname(output_metrics_path), exist_ok=True)
    with open(output_metrics_path, "w") as f:
        json.dump(metrics, f)
    print(f"Model accuracy: {accuracy}")
    print(f"Evaluation metrics saved at {output_metrics_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_path", type=str, default="/opt/ml/processing/input/model/model.joblib")
    parser.add_argument("--test_data_path", type=str, default="/opt/ml/processing/input/test_data/test.csv")
    parser.add_argument("--output_metrics_path", type=str, default="/opt/ml/processing/output/metrics/evaluation.json")
    args = parser.parse_args()

    evaluate_model(args.model_path, args.test_data_path, args.output_metrics_path)