---
challenge:
    module: 'Trigger GitHub Actions with feature-based development for Vertex AI'
    challenge: '3: Trigger GitHub Actions with feature-based development for Vertex AI'
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

# Challenge 3: Trigger GitHub Actions with feature-based development for Vertex AI

<button class="button" onclick="window.location.href='https://cloud.google.com/vertex-ai/docs';">Back to overview</button>

## Challenge scenario

Triggering a workflow by pushing directly to the main branch of a repository is generally discouraged. A preferred approach involves reviewing changes through pull requests before integrating them.

## Prerequisites

If you haven't, complete the [previous challenge](02-github-actions.md) before you continue.

## Objectives

By completing this challenge, you'll learn how to:

- Implement feature-based development practices.
- Protect the main branch of a repository.
- Trigger a GitHub Actions workflow upon the creation of a pull request.

> **Important!**
> Each challenge is designed to allow you to explore how to implement DevOps principles when working with machine learning models. Some instructions may be intentionally vague, inviting you to think about your own preferred approach. If, for example, the instructions ask you to interact with Vertex AI, it's up to you to explore and decide how you want to accomplish the task. To make it the best learning experience for you, it's up to you to make it as simple or as challenging as you want.

## Challenge Duration

- **Estimated Time**: 45 minutes

## Instructions

Adopt a feature-based development workflow to better manage changes to your repository and control the execution of GitHub Actions.

- Create a GitHub Actions workflow that is automatically triggered when a new pull request is created.

    This workflow will serve as a foundation for code verification in subsequent challenges. For now, include a placeholder step, such as an echo command, to signify where code checks will be implemented:

```yaml
    - name: Placeholder
      run: |
        echo "Code checks will be added here in the next challenge"
```

- Configure a branch protection rule to prevent direct pushes to the main branch, enforcing that all changes must be submitted via pull requests.

> **Note:**
> Branch protection rules typically do not apply to repository administrators. If you have administrative privileges, you may still be able to bypass these rules and push directly to the main branch.

To activate the workflow, perform the following steps:

- Create a new branch in your repository.
- Introduce a change to the code, such as modifying a hyperparameter value, and push this change to your branch.
- Initiate a pull request to merge the changes from your branch into the main branch.

## Success criteria

To successfully complete this challenge, you should be able to demonstrate:

- A configured branch protection rule for the main branch that prevents direct pushes.
- A GitHub Actions workflow that is triggered by the creation of a pull request and completes successfully.

## Useful resources

- Learn about source control best practices for machine learning projects and how to implement feature-based development using GitHub repositories.
- Refer to the official GitHub Actions documentation for comprehensive guidance on setting up and managing workflows.
- Explore the documentation on triggering workflows to understand how to automate actions based on various repository events.
- Consult the workflow syntax documentation for detailed information on constructing and customizing your GitHub Actions workflows.
- [Vertex AI Documentation](https://cloud.google.com/vertex-ai/docs)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

<button class="button" onclick="window.location.href='04-unit-test-linting.md';">Continue with challenge 4</button>