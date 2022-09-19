# Deployment Strategy (Rolling Update Deployment)
(**e: 9/18**) We decided against adopting blue green deployments for our service due to the cost of maintaining a single Kubernetes cluster in GKE. Due to the financial constraint, we decided to look into other deployment strategies.

This document briefly outlines the deployment strategy, or how deployments should be orchestrated for our API. For our deployment strategy, we chose rolling update deployments.

## Rolling Update Deployment
[Rolling update deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#rolling-update-deployment) is a deployment strategy that updates pods in a rolling/incremental fashion. With this strategy, we gradually rollout the new release version. The following is a broad outline of the steps that will be taken with our deployment strategy:
1. Smoke tests should be performed in development on a feature branch, in order to verify the stability of a build.
2. After changes are merged into the main branch, a new deployment should be made in the production environment.
3. From the production environment, test cases against new features, regression against existing features, and load tests should be verified.
   1. (**e: 9/18**) We currently do not have any plans for load testing on this service since we do not anticipate traffic on a large scale. Unit and integration tests are already adopted into the CD pipeline, which is usually sufficient before deployments.

We chose the rolling update deployment strategy for the following reasons:
- **Minimal effort for environment setup**: Since rolling update deployments iteratively update the pods on our existing Kubernetes cluster, no additional work on environment changes is needed for rolling updates.
- **Cost effective**: Our former decision for our deployment strategy was to use [blue green deployments](https://cloud.google.com/architecture/implementing-deployment-and-testing-strategies-on-gke#perform_a_bluegreen_deployment). Since blue green deployments require the overhead of a duplicate production environment, this initial strategy was not cost effective. Rolling update deployments instead allow us to handle deployments of our service with a single Kubernetes cluster.
- **Easy to understand**: Since rolling update deployments update an existing Kubernetes cluster, it only depends on two parameters:
  - **Max surge**: When updating our Kubernetes cluster, this parameter determines how many pods can be added to our cluster beyond the desired number of replicas. Depending on the scale of our cluster, this parameter determines how quickly pods running the newer version of our service can be provisioned.
  - **Max unavailable**: When updating our Kubernetes cluster, this parameter determines at minimum how many pods need to be available for serving traffic. Max unavailable is included in rolling update deployments in order to preserve the horizontal scale of our service during the deployment phase.
- **Quick to implement**: By default, Kubernetes uses rolling update deployments if no strategy is included in the deployment spec of our resource file. Since we initially did not specify a strategy, rolling update deployment is already supported.

