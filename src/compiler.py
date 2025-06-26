"""
Compiles KFP v2 pipelines to YAML for Vertex AI.
Supports both dev and prod pipelines with model registration.
"""

import argparse
from kfp.v2 import compiler

from vertex_pipeline_dev import dev_diabetes_pipeline
from vertex_pipeline_prod import prod_diabetes_pipeline


def main():
    parser = argparse.ArgumentParser(description="Compile a KFP v2 pipeline for Vertex AI.")
    parser.add_argument("--py", type=str, required=True, help="Path to the Python file defining the pipeline.")
    parser.add_argument("--output", type=str, required=True, help="Path to the output compiled YAML file.")
    args = parser.parse_args()

    # Best practice: Explicitly select the pipeline function based on the file name
    if "dev" in args.py:
        pipeline_func = dev_diabetes_pipeline
    elif "prod" in args.py:
        pipeline_func = prod_diabetes_pipeline
    else:
        raise ValueError("Pipeline file must be for 'dev' or 'prod'.")

    # Compile the selected pipeline function to YAML for Vertex AI Pipelines (KFP v2)
    compiler.Compiler().compile(
        pipeline_func=pipeline_func,
        package_path=args.output
    )


if __name__ == "__main__":
    main()