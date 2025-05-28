"""
Preprocessing script for SageMaker ProcessingStep.
Loads raw data, splits into train/test, and saves the results.
"""

import argparse
import pandas as pd
import os

def preprocess_data(input_path, output_train, output_test):
    print(f"Loading dataset from {input_path}")
    df = pd.read_csv(os.path.join(input_path, "diabetes.csv"))

    # Split data
    train_data = df.sample(frac=0.8, random_state=42)
    test_data = df.drop(train_data.index)

    # Save splits
    train_data.to_csv(output_train, index=False)
    test_data.to_csv(output_test, index=False)
    print("Data preprocessing complete!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_path", type=str, default="/opt/ml/processing/input/")
    parser.add_argument("--output_train", type=str, default="/opt/ml/processing/output/train/train.csv")
    parser.add_argument("--output_test", type=str, default="/opt/ml/processing/output/test/test.csv")
    args = parser.parse_args()

    preprocess_data(args.input_path, args.output_train, args.output_test)