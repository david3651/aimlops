"""
Compiles Kubeflow Pipelines (KFP v2) into YAML pipeline specs for Vertex AI.
Supports dev and prod variants of the diabetes prediction pipeline with dynamic selection.
"""

import argparse
import sys
from typing import Callable
from kfp.v2 import compiler
from kfp.dsl import Pipeline

from vertex_pipeline_dev import dev_diabetes_pipeline
from vertex_pipeline_prod import prod_diabetes_pipeline


def main() -> None:
    """
    Parses command-line arguments and compiles the selected pipeline
    into a YAML file suitable for Vertex AI Pipelines.
    """
    parser = argparse.ArgumentParser(
        description="Compile a KFP v2 pipeline for Vertex AI."
    )
    parser.add_argument(
        "--py",
        type=str,
        required=True,
        help="Path to the Python file defining the pipeline."
    )
    parser.add_argument(
        "--output",
        type=str,
        required=True,
        help="Path to the output compiled YAML file."
    )
    args = parser.parse_args()

    pipeline_func: Callable[..., Pipeline]

    # Select pipeline function based on filename
    if "vertex_pipeline_dev.py" in args.py:
        pipeline_func = dev_diabetes_pipeline
    elif "vertex_pipeline_prod.py" in args.py:
        pipeline_func = prod_diabetes_pipeline
    else:
        raise ValueError(
            f"Unknown pipeline file specified: {args.py}. "
            "Must contain 'vertex_pipeline_dev.py' or "
            "'vertex_pipeline_prod.py'."
        )

    try:
        compiler.Compiler().compile(
            pipeline_func=pipeline_func,
            package_path=args.output
        )
        print(f"✅ Successfully compiled '{args.py}' → '{args.output}'")
    except Exception as e:
        print(f"❌ Failed to compile pipeline: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
