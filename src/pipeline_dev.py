"""
Enhanced SageMaker Pipeline for Development
- Adds evaluation and conditional approval steps.
- Stores evaluation metrics in S3 for tracking and gating.
"""

from sagemaker.workflow.pipeline import Pipeline
from sagemaker.workflow.steps import ProcessingStep, TrainingStep
from sagemaker.workflow.parameters import ParameterString, ParameterFloat
from sagemaker.sklearn.processing import SKLearnProcessor
from sagemaker.sklearn.estimator import SKLearn
from sagemaker.inputs import TrainingInput
from sagemaker.processing import ProcessingInput, ProcessingOutput
from sagemaker.workflow.properties import PropertyFile
from sagemaker.workflow.conditions import ConditionGreaterThanOrEqualTo
from sagemaker.workflow.condition_step import ConditionStep

# Pipeline parameters
input_data_s3 = ParameterString(name="InputDataS3", default_value="s3://your-bucket/dev-data/")
training_instance_type = ParameterString(name="TrainingInstanceType", default_value="ml.c5.2xlarge")
reg_rate = ParameterFloat(name="RegRate", default_value=0.05)
min_accuracy_value = ParameterFloat(name="MinAccuracyValue", default_value=0.80)
role = "<your-sagemaker-execution-role-arn>"

# Data processing step
sk_processor = SKLearnProcessor(framework_version="0.23-1", role=role, instance_type="ml.m5.large", instance_count=1)
processing_step = ProcessingStep(
    name="DataPreprocessingStep",
    processor=sk_processor,
    inputs=[ProcessingInput(source=input_data_s3, destination="/opt/ml/processing/input/")],
    outputs=[
        ProcessingOutput(source="/opt/ml/processing/output/train", destination="s3://your-bucket/train/"),
        ProcessingOutput(source="/opt/ml/processing/output/test", destination="s3://your-bucket/test/")
    ]
)

# Training step
sk_estimator = SKLearn(
    entry_point="train.py",
    source_dir="src",
    role=role,
    instance_type=training_instance_type,
    hyperparameters={"reg_rate": reg_rate}
)
training_step = TrainingStep(
    name="TrainingStep",
    estimator=sk_estimator,
    inputs={
        "train": TrainingInput(s3_data=processing_step.properties.ProcessingOutputConfig.Outputs["train"].S3Output.S3Uri)
    }
)

# Evaluation step
evaluation_step_dev = ProcessingStep(
    name="EvaluateDevModel",
    processor=sk_processor,
    code="evaluate.py",
    inputs=[
        ProcessingInput(
            source=training_step.properties.ModelArtifacts.S3ModelArtifacts,
            destination="/opt/ml/processing/input/model"
        ),
        ProcessingInput(
            source=processing_step.properties.ProcessingOutputConfig.Outputs["test"].S3Output.S3Uri,
            destination="/opt/ml/processing/input/test_data"
        )
    ],
    outputs=[
        ProcessingOutput(
            source="/opt/ml/processing/output/metrics",
            destination="s3://your-bucket/dev-metrics/"
        )
    ],
    property_files=[
        PropertyFile(name="EvaluationReport", output_name="metrics", path="evaluation.json")
    ]
)

# Accuracy condition for approval
accuracy_condition_dev = ConditionGreaterThanOrEqualTo(
    left= evaluation_step_dev.properties.ProcessingOutputConfig.Outputs["metrics"].S3Output.S3Uri,
    right=min_accuracy_value
)

approval_step_dev = ConditionStep(
    name="ModelApprovalConditionDev",
    conditions=[accuracy_condition_dev],
    if_steps=[training_step],  # Proceed if accuracy meets threshold
    else_steps=[]
)

# Assemble the pipeline
pipeline_dev = Pipeline(
    name="MLopsCronosPipelineDev",
    parameters=[input_data_s3, training_instance_type, reg_rate, min_accuracy_value],
    steps=[processing_step, training_step, evaluation_step_dev, approval_step_dev]
)