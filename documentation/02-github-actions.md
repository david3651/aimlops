---
challenge:
    module: 'Trigger Vertex AI Custom Training Jobs with GitHub Actions'
    challenge: '2: Trigger a Vertex AI Custom Training Job with GitHub Actions'
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

# Challenge 2: Trigger a Vertex AI Custom Training Job with GitHub Actions

<button class="button" onclick="window.location.href='https://cloud.google.com/vertex-ai/docs';">Back to overview</button>

## Challenge scenario

The benefit of using the Vertex AI SDK to run a Custom Training Job is that you can submit the job from anywhere. Using a platform like GitHub will allow you to automate Vertex AI Custom Training Jobs. To trigger the job to run, you can use GitHub Actions.

## Prerequisites

If you haven't, complete the [previous challenge](01-aml-job.md) before you continue.

To complete the challenge, you need to have the authorization to create a service account and grant it necessary permissions.

## Objectives

By completing this challenge, you'll learn how to:

- Create a Google Cloud service account and use it to create a GitHub secret for authentication.
- Run a Vertex AI Custom Training Job with GitHub Actions.

> **Important!**
> Each challenge is designed to allow you to explore how to implement DevOps principles when working with machine learning models. Some instructions may be intentionally vague, inviting you to think about your own preferred approach. If for example, the instructions ask you to create a Vertex AI Workbench instance, it's up to you to explore and decide how you want to create it. To make it the best learning experience for you, it's up to you to make it as simple or as challenging as you want.

## Challenge Duration

- **Estimated Time**: 45 minutes

## Instructions

In the **.github/workflows** folder, you'll find the `02-manual-trigger.yml` file. The file defines a GitHub Action which can be manually triggered. The workflow checks out the repo onto the runner, and you will need to update it to authenticate with Google Cloud using a service account and run your training job.

- Create a Google Cloud service account with the necessary permissions (e.g., `roles/aiplatform.user`, `roles/storage.objectAdmin`) for Vertex AI and Cloud Storage. You can use the Cloud Shell in the Google Cloud Console.

    **Save the output**, you'll *also* need it for later challenges.  Update the `<your-project-id>` and `<service-account-name>` (should be unique) before using the following command:
```bash
    gcloud iam service-accounts create <service-account-name> \
        --project=<your-project-id>

    gcloud projects add-iam-policy-binding <your-project-id> \
        --member="serviceAccount:<service-account-name>@<your-project-id>.iam.gserviceaccount.com" \
        --role="roles/aiplatform.user"

    gcloud projects add-iam-policy-binding <your-project-id> \
        --member="serviceAccount:<service-account-name>@<your-project-id>.iam.gserviceaccount.com" \
        --role="roles/storage.objectAdmin"

    gcloud iam service-accounts keys create ./service_account.json \
        --iam-account=<service-account-name>@<your-project-id>.iam.gserviceaccount.com
```
    **Note**: This script downloads a service account key file (`service_account.json`). **Handle this file with extreme care and do not commit it to your repository.** It will be used to create a GitHub secret.

- Create a GitHub secret in your repository. Name it `GCP_CREDENTIALS` and copy and paste the *contents* of the `service_account.json` file you downloaded into the **Value** field of the secret.

- Edit the `02-manual-trigger.yml` workflow to trigger the Vertex AI Custom Training Job you defined in challenge 1. You'll need to:
    - Add a step to authenticate with Google Cloud using the `GCP_CREDENTIALS` secret. You can use the `google-github-actions/auth` action for this.
    - Add a step to run your training script (e.g., `python src/model/train.py`) within the appropriate environment and with the necessary arguments for your Vertex AI Custom Training Job.  You might need to install dependencies using a `requirements.txt` file in a previous step.

> **Tip:** Refer to the Vertex AI documentation on running custom training jobs for guidance on the necessary arguments and environment setup.

## Success criteria

To complete this challenge successfully, you should be able to show:

- A successfully completed Action in your GitHub repo, triggered manually in GitHub.
- A step in the Action should have submitted a Custom Training Job to Vertex AI.
- A successfully completed Vertex AI Custom Training Job, shown in the Vertex AI console, with the expected input parameters and output metrics.

## Useful resources

- [Vertex AI Custom Training Documentation](https://cloud.google.com/vertex-ai/docs/training/custom-training)
- [Vertex AI Python SDK Documentation](https://cloud.google.com/python/docs/reference/aiplatform/latest)
- [Authenticating to Google Cloud with GitHub Actions](https://github.com/google-github-actions/auth)
- [Setting up Workflows with GitHub Actions](https://docs.github.com/en/actions/using-workflows)
- [Managing Secrets in GitHub Actions](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [Google Cloud IAM Documentation](https://cloud.google.com/iam/docs)