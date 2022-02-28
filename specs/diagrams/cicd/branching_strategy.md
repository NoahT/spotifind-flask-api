# Branching Strategy (GitHub flow)
This document briefly outlines [GitHub flow](https://docs.github.com/en/get-started/quickstart/github-flow), which is the branching strategy chosen for this project. Our branching strategy determines the manner in which we will make and merge changes to this project with Git version control.

## GitHub flow
GitHub flow is a lightweight and simplified version control model. The overarching idea for this branching model is that all development occurs off a single trunk branch, with pull requests targeting the trunk in order to merge and verify the integrity of new changes. This branching model is nearly identical to [trunk based development](https://trunkbaseddevelopment.com/), with the exception of short lived feature branches and pull requests for merging changes. Since our branching strategy is GitHub flow, the following outlines the necessary steps that should be performed for all changes:
1. Create a new feature branch. This feature branch should be created off of the trunk branch *main*.
2. Make all relevant changes on the feature branch, merging new changes from the trunk when appropriate.
3. When changes to the feature branch are ready, raise a pull request to target the trunk. It is during this step that relevant CI jobs should run for formatting, unit tests, and integration tests. If applicable peer review is also performed.
4. After the mentioned conditions in the above step are fulfilled, changes can be merged into the trunk.

We choose GitHub flow for this project due to the following reasons:
- **Minimal effort for CI setup**: Since pull requests target a centralized branch in our project, GitHub Flow does not require significant effort for CI setup.
- **Reduced risk for branch divergence**: All work happens on short-lived feature branches close to the trunk, which mitigates the chance of merge conflicts.
- **Easy to understand**: GitHub flow is a straightforward and easy to learn branching strategy.
- **Frequently used and well documented**: GitHub flow is a popular branching strategy, with lots of documentation for setting up a CI/CD pipeline.

