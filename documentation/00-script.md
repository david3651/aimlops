---
challenge:
    module: Convert a notebook to production code
    challenge: '0: Convert a notebook to production code'
---

<style>
.button  {
  border: none;
  color: white;
  padding: 12px 28px;
  background-color: #FF9900;
  float: right;
}
</style>

# Challenge 0: Convert a notebook to production code

<button class="button" onclick="window.location.href='https://aws.amazon.com/sagemaker/mlops/';">Back to overview</button>

## Challenge scenario

The first step to automate machine learning workflows is to convert a Jupyter notebook to production-ready code. When you store your code as scripts, it's easier to automate the code execution. You can parameterize scripts to easily reuse the code for retraining with Amazon SageMaker.

## Prerequisites

To complete this challenge, you'll need:

- Access to an AWS account with appropriate permissions.
- A GitHub account.
- Basic familiarity with Amazon SageMaker and AWS services.

## Objectives

By completing this challenge, you'll learn how to:

- Clean nonessential code.
- Convert your code to Python scripts compatible with SageMaker.
- Use functions in your scripts.
- Use parameters in your scripts.
- Implement experiment tracking with SageMaker Experiments.

> **Important!**
> Each challenge is designed to allow you to explore how to implement DevOps principles when working with machine learning models on AWS. Some instructions may be intentionally vague, inviting you to think about your own preferred approach. If for example, the instructions ask you to create a SageMaker domain or notebook instance, it's up to you to explore and decide how you want to create it. To make it the best learning experience for you, it's up to you to make it as simple or as challenging as you want.

## Challenge Duration

- **Estimated Time**: 30 minutes

## Instructions

To work through the challenges, you need **your own public repo** which includes the challenge files. Create a new public repo by navigating to [https://github.com/aws-samples/sagemaker-mlops-workshop](https://github.com/aws-samples/sagemaker-mlops-workshop) and fork or use as a template to create your own repo.

In the **experimentation** folder, you'll find a Jupyter notebook that trains a classification model. The data used by the notebook is in the **experimentation/data** folder and contains a CSV file.

In the **src/model** folder you'll find a `train.py` script which already includes code converted from part of the notebook. It's up to you to complete it for SageMaker compatibility.

- Go through the notebook to understand what the code does.
- Convert the code under the **Split data** header and include it in the `train.py` script as a `split_data` function. Remember to:
    - Remove nonessential code.
    - Include the necessary code as a function.
    - Include any necessary libraries at the top of the script.
    - Ensure compatibility with SageMaker's training environment.

<details>
<summary>Hint</summary>
<br/>
The <code>split_data</code> function is already included in the main function. You only need to add the function itself with the required inputs and outputs underneath the comment <code>TO DO: add function to split data</code>. Make sure to handle SageMaker's expected input/output paths using environment variables like <code>SM_MODEL_DIR</code> and <code>SM_CHANNEL_TRAINING</code>.
</details>

- Add experiment tracking so that every time you run the script, all parameters and metrics are tracked. Use SageMaker Experiments to track your training runs, or alternatively, integrate with MLflow on SageMaker to ensure the necessary model files are stored with the job run for easy deployment.

<details>
<summary>Hint</summary>
<br/>
SageMaker provides native experiment tracking capabilities through SageMaker Experiments. You can also use MLflow with SageMaker for experiment tracking. For SageMaker Experiments, use the SageMaker Python SDK to create and track experiments. For MLflow integration, you can use <code>mlflow.autolog()</code> with SageMaker's managed MLflow tracking server. Enable experiment tracking in the main function under <code>TO DO: enable experiment tracking</code>.
</details>

- Ensure your script is compatible with SageMaker training jobs by:
    - Using SageMaker environment variables for input/output paths
    - Saving the model to the correct output directory (`/opt/ml/model/`)
    - Adding proper argument parsing for hyperparameters

<details>
<summary>Hint</summary>
<br/>
SageMaker provides specific environment variables like <code>SM_MODEL_DIR</code>, <code>SM_CHANNEL_TRAINING</code>, and <code>SM_NUM_GPUS</code>. Use these to make your script portable across different SageMaker environments. Also, implement argument parsing using <code>argparse</code> to handle hyperparameters passed from SageMaker training jobs.
</details>

## Success criteria

To complete this challenge successfully, you should be able to show:

- A training script which includes a function to split the data and experiment tracking using SageMaker Experiments or MLflow.
- The script is compatible with SageMaker training jobs (uses appropriate environment variables and paths).
- Proper model serialization and saving to SageMaker's expected output directory.

> **Note:**
> If you've used a SageMaker notebook instance or SageMaker Studio for experimentation, remember to stop the instance when you're done to avoid unnecessary charges.

## Useful resources

- [Amazon SageMaker Developer Guide - Using Scikit-learn with SageMaker](https://docs.aws.amazon.com/sagemaker/latest/dg/sklearn.html)
- [SageMaker Experiments for Experiment Tracking](https://docs.aws.amazon.com/sagemaker/latest/dg/experiments.html)
- [Using MLflow with Amazon SageMaker](https://docs.aws.amazon.com/sagemaker/latest/dg/mlflow.html)
- [SageMaker Training Toolkit](https://github.com/aws/sagemaker-training-toolkit)
- [SageMaker Python SDK Documentation](https://sagemaker.readthedocs.io/)
- [AWS Machine Learning Blog - MLOps Best Practices](https://aws.amazon.com/blogs/machine-learning/)

<button class="button" onclick="window.location.href='01-sagemaker-job';">Continue with challenge 1</button>