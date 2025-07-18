---
challenge:
    module: 'Work with linting and unit testing in GitHub Actions for Vertex AI'
    challenge: '4: Work with linting and unit testing for Vertex AI'
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

# Challenge 4: Work with linting and unit testing for Vertex AI

<button class="button" onclick="window.location.href='https://cloud.google.com/vertex-ai/docs';">Back to overview</button>

## Challenge scenario

Ensuring code quality is crucial for reliable machine learning workflows. This can be achieved through linting to identify stylistic issues and unit testing to verify the functionality of individual components.

## Prerequisites

If you haven't, complete the [previous challenge](03-trigger-workflow.md) before you continue.

You will be working with and expanding on the workflow created in the previous challenge.

## Objectives

By completing this challenge, you'll learn how to:

- Configure and execute linters and unit tests within a GitHub Actions workflow.
- Interpret and address linting and unit test results to enhance code quality.

> **Important!**
> Each challenge is designed to allow you to explore how to implement DevOps principles when working with machine learning models on Google Cloud. Some instructions may be intentionally vague, inviting you to think about your own preferred approach. If, for example, the instructions ask you to interact with Vertex AI, it's up to you to explore and decide how you want to accomplish the task. To make it the best learning experience for you, it's up to you to make it as simple or as challenging as you want.

## Challenge Duration

- **Estimated Time**: 45 minutes

## Instructions

Within the **tests** folder, you'll find the necessary files to perform linting and unit testing on your code. `flake8` will analyze your code for stylistic inconsistencies, while `test_train.py` contains unit tests to validate the behavior of your functions.

- Access the **Actions** tab in your GitHub repository and manually trigger the **Code checks** workflow. Examine the output for any reported issues and address them accordingly.

<details>
<summary>Hint</summary>
<br/>
Linting errors will cause the GitHub Actions step to fail with a non-zero exit code. Carefully review the workflow output to identify specific error codes and associated file, line, and column information to pinpoint and resolve the issues.
</details>

- Integrate linting and unit testing into the workflow established in the previous challenge. Configure the workflow to be triggered upon the creation of a new pull request. The workflow should execute both the Flake8 linter and Pytest unit tests.

<details>
<summary>Hint</summary>
<br/>
To incorporate unit testing, ensure Pytest is installed (refer to <code>requirements.txt</code>) and execute the tests using the command <code>pytest tests/</code>. Pytest automatically discovers test files prefixed with <code>test</code>.
</details>

- Establish (or modify) a **branch protection rule** to enforce successful completion of both code checks before allowing pull requests to be merged into the **main** branch.

<details>
<summary>Hint</summary>
<br/>
Enable <b>status checks</b> within the branch protection rule to mandate successful completion of specified checks before merging. Ensure your jobs have descriptive names for easy identification. The workflow, triggered by a <code>pull_request</code> event, should include these checks as distinct jobs.
</details>

To initiate the workflow, follow these steps:

- Introduce a change and push it to your branch. For instance, modify a hyperparameter value.
- Create a pull request to observe the integrated code checks in action.

## Success criteria

To successfully complete this challenge, you should be able to demonstrate:

- The successful completion of both **Linting** and **Unit tests** checks without any reported errors. Evidence of these successful checks should be visible within a newly created pull request.

## Useful resources

- Explore the [Flake8 documentation](https://flake8.pycqa.org/latest/user/index.html) and refer to the detailed [error codes and descriptions](https://flake8.pycqa.org/en/latest/user/error-codes.html).
- Refer to [a beginner's guide to Python testing](https://miguelgfierro.com/blog/2018/a-beginners-guide-to-python-testing) for foundational knowledge.
- Enhance your understanding of testing with [Pytest](https://docs.pytest.org/en/7.x/), and explore advanced testing strategies.
- [Vertex AI Documentation](https://cloud.google.com/vertex-ai/docs)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

In this challenge, all testing is executed within GitHub Actions. While not mandatory for this challenge, you can optionally investigate methods to verify your code locally.

<button class="button" onclick="window.location.href='05-environments.md';">Continue with challenge 5</button>