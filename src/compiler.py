"""
Compiles KFP pipelines to YAML or JSON format for Vertex AI.
"""

import argparse
from kfp.v2 import compiler

from vertex_pipeline_dev import dev_diabetes_pipeline
from vertex_pipeline_prod import prod_diabetes_pipeline


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--py", type=str, required=True, help="Path to the Python file defining the pipeline.")
    parser.add_argument("--output", type=str, required=True, help="Path to the output compiled YAML file.")
    args = parser.parse_args()

    if "dev" in args.py:
        compiler.Compiler().compile(pipeline_func=dev_diabetes_pipeline, package_path=args.output)
    elif "prod" in args.py:
        compiler.Compiler().compile(pipeline_func=prod_diabetes_pipeline, package_path=args.output)
    else:
        raise ValueError("Pipeline file must be for 'dev' or 'prod'.")

if __name__ == "__main__":
    main()