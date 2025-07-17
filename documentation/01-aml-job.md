---
---
challenge:
    module: Use a Vertex AI Custom Training Job for Automation
    challenge: '1: Create a Vertex AI Custom Training Job'
---

<style>
.button  {
  border: none;
  color: white;
  padding: 12px 28px;
  background-color: #4285F4; /* Updated button color to Google Blue */
  float: right;
}
</style>

# Challenge 1: Create a Vertex AI Custom Training Job

<button class="button" onclick="window.location.href='https://cloud.google.com/vertex-ai/docs';">Back to overview</button>

## Challenge scenario

To automate machine learning workflows, you can define machine learning tasks in scripts. To execute any workflow consisting of Python scripts, use Vertex AI Custom Training Jobs. Vertex AI Custom Training Jobs store all metadata of a workflow, including input parameters and output metrics. By running scripts as jobs, it's easier to track and manage your machine learning models.

## Prerequisites

If you haven't, complete the [previous challenge](00-gscript.md) before you continue.

## Objectives

By completing this challenge, you'll learn how to:

- Define a Vertex AI Custom Training Job using the Vertex AI SDK.
- Run a Vertex AI Custom Training Job.

> **Important!**
> Each challenge is designed to allow you to explore how to implement DevOps principles when working with machine learning models. Some instructions may be intentionally vague, inviting you to think about your own preferred approach. If for example, the instructions ask you to create a Vertex AI Workbench instance, it's up to you to explore and decide how you want to create it. To make it the best learning experience for you, it's up to you to make it as simple or as challenging as you want.

## Challenge Duration

- **Estimated Time**: 30 minutes

## Instructions

In the **src/model** folder, you'll find a Python script (`train.py`) which reads CSV files from a folder in Google Cloud Storage (GCS) and uses the data to train a classification model.

- Create a Vertex AI Workbench instance.
- Upload the contents of your `experimentation/data` folder to a Google Cloud Storage (GCS) bucket.

- Use the Vertex AI SDK to create and submit a Custom Training Job. You will not need a separate YAML file, as the job will be defined and launched directly through Python code in your Workbench instance. The key steps are:
    - **Define a `CustomTrainingJob`:**  Specify the training script path (`src/model/train.py`), the entrypoint function, and the container image to use for the training environment. Consider using a prebuilt container or building your own.
    - **Define a `WorkerPoolSpec`:** Configure the machine type, accelerator type (if needed), and replica count for your training job.
    - **Create a `CustomJob` instance:** Combine the `CustomTrainingJob` and `WorkerPoolSpec` to create a `CustomJob` object.
    - **Submit the job:** Use the `run()` method of the `CustomJob` object to submit the training job to Vertex AI.  Pass in the GCS path to your training data, any hyperparameters for your training script, and other relevant configurations like the GCS staging bucket for outputs and experiment tracking settings.

> **Tip:**  Refer to the Vertex AI Python SDK documentation and examples for detailed guidance on creating and running Custom Training Jobs. You can find links to relevant resources in the "Useful Resources" section below.

## Success criteria

To complete this challenge successfully, you should be able to show:

- A successfully completed Custom Training Job in the Vertex AI console. The job details should include the input parameters, output metrics, training data path, and a link to the trained model artifacts in GCS.

> **Note:**
> If you've used a Vertex AI Workbench instance for experimentation, remember to stop the instance when you're done to avoid unnecessary charges. Also, clean up any Google Cloud Storage buckets and Vertex AI resources you created during testing.

## Useful resources

- [Vertex AI Custom Training Documentation](https://cloud.google.com/vertex-ai/docs/training/custom-training)
- [Vertex AI Python SDK Documentation](https://cloud.google.com/python/docs/reference/aiplatform/latest)
- [Vertex AI Workbench User Guide](https://cloud.google.com/vertex-ai/docs/workbench)
- [Google Cloud Storage Client Libraries](https://cloud.google.com/storage/docs/reference/libraries)
- [Example Notebooks for Vertex AI Training](https://github.com/GoogleCloudPlatform/vertex-ai-samples/tree/main/notebooks/official/training)

<button class="button" onclick="window.location.href='02-github-actions.md';">Continue with challenge 2</button>
