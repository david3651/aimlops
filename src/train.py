"""
Training script for SageMaker TrainingStep.
Trains a logistic regression model and saves the model artifact.
"""

import argparse
import pandas as pd
import joblib
from sklearn.linear_model import LogisticRegression
import os

def train_model(training_data_path, output_model_path, reg_rate):
    print("Loading training data...")
    train_data = pd.read_csv(training_data_path)

    columns = ['Pregnancies', 'PlasmaGlucose', 'DiastolicBloodPressure',
               'TricepsThickness', 'SerumInsulin', 'BMI', 'DiabetesPedigree', 'Age']
    X_train = train_data[columns]
    y_train = train_data['Diabetic']

    model = LogisticRegression(C=1 / reg_rate, solver="liblinear")
    model.fit(X_train, y_train)

    os.makedirs(os.path.dirname(output_model_path), exist_ok=True)
    joblib.dump(model, output_model_path)
    print(f"Model trained and saved at {output_model_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--training_data_path", type=str, default="/opt/ml/input/data/train/train.csv")
    parser.add_argument("--output_model_path", type=str, default="/opt/ml/model/model.joblib")
    parser.add_argument("--reg_rate", type=float, default=0.05)
    args = parser.parse_args()

    train_model(args.training_data_path, args.output_model_path, args.reg_rate)