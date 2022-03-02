# Release Strategy (Blue Green)
This document briefly outlines the release strategy, or how deployments should be orchestrated for our API. For our release strategy, we chose blue green deployments.

## Blue Green Deployment
[Blue green deployment](https://www.redhat.com/en/topics/devops/what-is-blue-green-deployment) is a deployment strategy that mirrors a production environment (the *green* environment) with a staging environment (the *blue* environment). User traffic is wired on to the production environment, while the following release is tested on staging. With this release strategy, QA will happen directly in staging after development. The following is a broad outline of the steps that will be taken with our release strategy:
1. Smoke tests should be performed in development on a feature branch, in order to verify the stability of a build.
2. After changes are merged into the main branch, a new deployment should be made in the staging environment.
3. From the staging environment, test cases against new features, regression against existing features, and load tests should be verified.
4. After the changes in QA are accepted, user traffic should shift from production to staging. User traffic can shift back to the former production environment if a rollback is needed.

We chose the blue green deployment strategy for the following reasons:
- **Minimal effort for environment setup**: Blue green deployments minimize the overhead from environment setup; we will only need a staging and production environment. Since our capacity estimates for this API are low, having two environments scaled for production-level traffic is not an issue.
- **Easy to understand**: Blue green deployment strategy is a relatively easy strategy to orchestrate for deployment.
- **Quick to implement**: Blue green deployment is not supported out of the box by K8s, but can be implemented directly. There are a lot of guides for supporting blue green deployment with plain kubectl commands.

