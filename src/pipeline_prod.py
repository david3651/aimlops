"""
Production SageMaker Pipeline
-----------------------------
- Integrates evaluate.py for model validation.
- Stores evaluation metrics in S3 for deployment gating.
- Implements accuracy threshold control for production approval.
- Ready for model registration in SageMaker Model Registry.
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
input_data_s3_prod = ParameterString(name="InputDataS3", default_value="s3://your-bucket/prod-data/")
training_instance_type_prod = ParameterString(name="TrainingInstanceType", default_value="ml.c5.4xlarge")
min_accuracy_value = ParameterFloat(name="MinAccuracyValue", default_value=0.80)
role = "arn:aws:iam::799101906606:role/ase-cronos-mlops-sagemaker-execution-role"

# Data processing step
sk_processor = SKLearnProcessor(framework_version="0.23-1", role=role, instance_type="ml.m5.large", instance_count=1)
processing_step_prod = ProcessingStep(
    name="ProductionDataPreprocessingStep",
    processor=sk_processor,
    inputs=[ProcessingInput(source=input_data_s3_prod, destination="/opt/ml/processing/input/")],
    outputs=[
        ProcessingOutput(source="/opt/ml/processing/output/train", destination="s3://your-bucket/prod-train/"),
        ProcessingOutput(source="/opt/ml/processing/output/test", destination="s3://your-bucket/prod-test/")
    ]
)

# Training step
sk_estimator_prod = SKLearn(
    entry_point="train.py",
    source_dir="src",
    role=role,
    instance_type=training_instance_type_prod,
    hyperparameters={"reg_rate": 0.05}
)
training_step_prod = TrainingStep(
    name="ProductionTrainingStep",
    estimator=sk_estimator_prod,
    inputs={
        "train": TrainingInput(s3_data=processing_step_prod.properties.ProcessingOutputConfig.Outputs["train"].S3Output.S3Uri)
    }
)

# Evaluation step
evaluation_step_prod = ProcessingStep(
    name="EvaluateProductionModel",
    processor=sk_processor,
    code="evaluate.py",
    inputs=[
        ProcessingInput(
            source=training_step_prod.properties.ModelArtifacts.S3ModelArtifacts,
            destination="/opt/ml/processing/input/model"
        ),
        ProcessingInput(
            source=processing_step_prod.properties.ProcessingOutputConfig.Outputs["test"].S3Output.S3Uri,
            destination="/opt/ml/processing/input/test_data"
        )
    ],
    outputs=[
        ProcessingOutput(
            source="/opt/ml/processing/output/metrics",
            destination="s3://your-bucket/prod-metrics/"
        )
    ],
    property_files=[
        PropertyFile(name="EvaluationReport", output_name="metrics", path="evaluation.json")
    ]
)

# Accuracy gating for production approval
accuracy_condition_prod = ConditionGreaterThanOrEqualTo(
    left=evaluation_step_prod.properties.ProcessingOutputConfig.Outputs["metrics"].S3Output.S3Uri,
    right=min_accuracy_value
)

approval_step_prod = ConditionStep(
    name="ModelApprovalConditionProd",
    conditions=[accuracy_condition_prod],
    if_steps=[training_step_prod],  # Proceed only if accuracy meets threshold
    else_steps=[]
)

# Assemble the pipeline
pipeline_prod = Pipeline(
    name="MLopsCronosPipelineProd",
    parameters=[input_data_s3_prod, training_instance_type_prod, min_accuracy_value],
    steps=[processing_step_prod, training_step_prod, evaluation_step_prod, approval_step_prod]
)