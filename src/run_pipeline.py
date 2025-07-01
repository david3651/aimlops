"""
Submits a Vertex AI Pipeline Job using the Vertex AI SDK for Python.

This script is the recommended, officially supported method for running
Vertex AI Pipelines from a CI/CD environment. It replaces the need for
the gcloud CLI for pipeline submission.
"""

import argparse
import json
import logging
from datetime import datetime
from google.cloud import aiplatform


def main():
    parser = argparse.ArgumentParser(
        description="Submit a Vertex AI Pipeline Job."
    )
    parser.add_argument(
        "--project-id", type=str, required=True, help="Google Cloud project ID."
    )
    parser.add_argument(
        "--region", type=str, required=True, help="Google Cloud region."
    )
    parser.add_argument(
        "--pipeline-spec-uri", type=str, required=True,
        help="GCS URI or local path of the compiled pipeline spec."
    )
    parser.add_argument(
        "--service-account", type=str, required=True,
        help="Service account for the pipeline run."
    )
    parser.add_argument(
        "--pipeline-root", type=str, required=True,
        help="GCS root path for pipeline outputs."
    )
    parser.add_argument(
        "--display-name", type=str, required=True,
        help="Display name for the pipeline run."
    )
    parser.add_argument(
        "--parameter-values-json", type=str, required=True,
        help="JSON string of pipeline parameter values."
    )
    parser.add_argument(
        "--labels-json", type=str, required=True,
        help="JSON string of labels for the pipeline run."
    )
    parser.add_argument(
        "--enable-caching", action="store_true",
        help="Flag to enable caching for the pipeline run."
    )

    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    logging.info("Initializing Vertex AI Platform...")

    aiplatform.init(project=args.project_id, location=args.region)

    try:
        parameter_values = json.loads(args.parameter_values_json)
        labels = json.loads(args.labels_json)
    except json.JSONDecodeError as e:
        logging.error(f"Failed to parse JSON arguments: {e}")
        raise

    job_id = f"{args.display_name}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    logging.info(f"Submitting pipeline job: {job_id}")

    pipeline_job = aiplatform.PipelineJob(
        display_name=job_id,
        template_path=args.pipeline_spec_uri,
        pipeline_root=args.pipeline_root,
        parameter_values=parameter_values,
        enable_caching=args.enable_caching,
        labels=labels
    )

    pipeline_job.submit(service_account=args.service_account)

    logging.info(f"✅ Successfully submitted pipeline job: {job_id}")
    logging.info(f"View in console: {pipeline_job._dashboard_uri()}")


if __name__ == "__main__":
    main()