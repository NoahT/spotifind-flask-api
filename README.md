# Spotifind REST API
REST API for recommending tracks and creating playlists on Spotify.

## Table of contents
- [Spotifind REST API](#spotifind-rest-api)
  - [Table of contents](#table-of-contents)
  - [Overview](#overview)
    - [How the recommendations work](#how-the-recommendations-work)
  - [Architecture for GET::/v1/reco/{id\*}](#architecture-for-getv1recoid)
  - [Architecture for POST::/v1/playlist/{user\_id\*}/{track\_id\*}](#architecture-for-postv1playlistuser_idtrack_id)
  - [API Documentation](#api-documentation)
    - [Endpoints](#endpoints)
    - [Resources](#resources)
      - [GET::/v1/reco/{id\*}](#getv1recoid)
        - [HTTP response status codes](#http-response-status-codes)
        - [Example Usage](#example-usage)
      - [POST::/v1/playlist/{user\_id\*}/{track\_id\*}](#postv1playlistuser_idtrack_id)
        - [HTTP response status codes](#http-response-status-codes-1)
        - [Request headers](#request-headers)
        - [Response headers](#response-headers)
        - [Example Usage](#example-usage-1)
  - [Contributions](#contributions)
    - [Installation](#installation)
    - [Development](#development)
      - [Branching strategy](#branching-strategy)
    - [Making changes](#making-changes)
    - [Testing](#testing)
      - [Unit testing](#unit-testing)
      - [Integration testing](#integration-testing)

## Overview
Spotifind is a REST web service that provides the ability to provide any number of Spotify track recommendations based on any available input track.

### How the recommendations work
(This is not needed to interface with the API, but it's an interesting read if you like machine learning, linear algebra, or distributed systems)

We motivate understanding by the following constraints imposed on our API:
- **No end user context**: We assume that we have no understanding of the end user's likes and dislikes. This cannot be exploited for incoming requests.
- **Recommendations on demand**: Recommendations need to be determined on-demand when an input track is received by calling clients. It consequently needs to adopt a low-latency strategy.

For the first contraint imposed above, in order to make recommendations, our API exploits a [content-based filtering](https://developers.google.com/machine-learning/recommendation/content-based/basics) machine learning strategy, where Spotify track recommendations are made based on the affinity to the input track. With respect to the second contraint, a nearest neighbors strategy naturally evolves from the need to provide recommendations on demand. Since we wish for recommendations to remain low-latent as the possible track recommendations scale, it uses [Vertex AI Matching Engine](https://cloud.google.com/vertex-ai/docs/matching-engine/overview); this allows our API to provide low-latency response times for any number of requested recommendations at a high scale.


Below is the current iteration for the system architecture for both APIs. The core components are outlined as follows:
- The recommender system sits behind the REST API which calling clients interface with. The resource on this API used to get recommendations is `GET::/v1/reco/{id*}`, where **id** denotes the input Spotify track ID.
- The recommender system downstream is contained inside of a [gRPC](https://grpc.io/) web service. A data lake is created containing Spotify track IDs and corresponding features from the Spotify [audio features](https://developer.spotify.com/console/get-audio-features-track/) API (liveness, tempo, danceability, etc.) with roughly 100,000 songs. Using these features, a special kind of vector space called a [feature space](https://pages.cs.wisc.edu/~bsettles/cs540/lectures/16_feature_spaces.pdf) is created containing an embedding (representation) of all Spotify tracks used for recommendation output. This data lake is used by the Vertex AI machine learning platform to build an index that is needed for low-latent nearest neighbors searches.
- For input songs, the [client credentials flow](https://developer.spotify.com/documentation/general/guides/authorization/client-credentials/) is used for authentication: a call to Spotify's `/api/token` API is made first, with a sequential service call being made to the Spotify [audio features](https://developer.spotify.com/console/get-audio-features-track/) API in order to embed the input song into our feature space. From here, our gRPC service takes this track embedding as input and returns the nearest neighbors as track embeddings for the recommended songs.
- For the `POST::/v1/playlist/{user_id*}/{track_id*}` API, Bearer token authentication is required: since the creation of playlists does not only make use of read-only operations on public resources, calling clients need to include the [Authorization](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Authorization) request header with [playlist-modify-public](https://developer.spotify.com/documentation/general/guides/authorization/scopes/#playlist-modify-public), [playlist-modify-private](https://developer.spotify.com/documentation/general/guides/authorization/scopes/#playlist-modify-private) scopes.

## Architecture for GET::/v1/reco/{id*}
[![Spotifind system architecture GET::/v1/reco/{id*}](specs/diagrams/architecture/component_diagram_get_v1_reco_id.drawio.png)](specs/diagrams/architecture/component_diagram_get_v1_reco_id.drawio.png)

## Architecture for POST::/v1/playlist/{user_id*}/{track_id*}
[![Spotifind system architecture POST::/v1/playlist/{user_id*}/{track_id*}](specs/diagrams/architecture/component_diagram_post_v1_playlist_id.drawio.png)](specs/diagrams/architecture/component_diagram_post_v1_playlist_id.drawio.png)

## API Documentation
Spotifind is a REST web service. Any HTTP client can be used in order to interface with the API. A Postman collection for the existing resources can be found [here](https://www.getpostman.com/collections/3227a5bf7a781f5bfd65).

### Endpoints
Spotifind API is exposed behind two endpoints. Note that HTTPS is the required protocol:

1. **spotifind-api.com**: This is our endpoint configured in Google Cloud.
2. **localhost (loopback address)**: This is used during development on a local machine.

### Resources

#### GET::/v1/reco/{id*}
Get recommendations for Spotify track URIs based on an input track URI.

| Resource  | Description | Type | Path parameters | Query parameters |
| ------------- | ------------- | ------------- | ------------- | ------------- |
| /v1/reco/{id*}  | Retrieve Spotify tracks to recommend based on the given track id | GET | **id** - Spotify Track ID to use when getting recommendations | **size** - Number of recommendations to return. Default size 5

##### HTTP response status codes
| Status code | Description |
| ------------- | ------------- |
| 200  | When track id recommendations are returned successfully |
| 400  | Miscellaneous client failure |
| 404  | Client failure due to invalid track id |
| 500  | Miscellaneous service failure |

##### Example Usage
**Request**
```
GET /v1/reco/62BGM9bNkNcvOh13B4wOyr?size=5 HTTPS/1.1
Host: spotifind-api.com
```

**Response (200)**
```
HTTPS/1.1 200 OK
Content-Type: application/json
. . . // Miscellaneous response headers

{
  "request": {
    "track": {
      "id": "62BGM9bNkNcvOh13B4wOyr"
    },
    "size": 5
  },
  "recos": [
    {
      "id": "2TRu7dMps7cVKOyazkj9Fb"
    },
    {
      "id": "0bqrFwY1HixfnusFxhYbDl"
    },
    {
      "id": "4BHSjbYylfOH5WAGusDyni"
    },
    {
      "id": "3s9f1LQ6607eDj9UYCzmgk"
    },
    {
      "id": "2HbKqm4o0w5wEeEFXm2sD4"
    }
  ]
}
```

**Request**
```
GET /v1/reco/62BGM9bNkNcvOh13B4wOyr?size=invalid_size HTTPS/1.1
Host: spotifind-api.com
```

**Response (400)**
```
HTTPS/1.1 400 BAD REQUEST
. . . // Miscellaneous response headers

{
  "error": {
    "status": 400,
    "message": "Bad request."
  }
}
```

**Request**
```
GET /v1/reco/invalid_id HTTPS/1.1
Host: spotifind-api.com
```

**Response (404)**
```
HTTPS/1.1 404 NOT FOUND
. . . // Miscellaneous response headers

{
  "error": {
    "status": 404,
    "message": "Invalid track id."
  }
}
```

#### POST::/v1/playlist/{user_id*}/{track_id*}
Create a Spotify playlist containing recommended Spotify track URIs based on an input track URI for a target user.

| Resource  | Description | Type | Path parameters | Query parameters |
| ------------- | ------------- | ------------- | ------------- | ------------- |
| /v1/playlist/{id*}  | Create Spotify playlist with recommended tracks based on the given track id | POST | **user_id** - Spotify user ID to generate the playlist for (i.e. noahteshima) <br> **track_id** - Spotify track ID to use when generating playlist | **size** - Size of the playlist to generate. Default size 5

##### HTTP response status codes
| Status code | Description |
| ------------- | ------------- |
| 201  | When Spotify playlist is created successfully |
| 400  | Miscellaneous client failure |
| 401  | Client failure due to missing `Authorization` header |
| 403  | Client failure due to insufficient scopes in `Authorization` header |
| 404  | Client failure due to invalid track id |
| 500  | Miscellaneous service failure |

##### Request headers
| Request header | Value(s) |
| ------------- | ------------- |
| Authorization  | Bearer {token}, where `token` is a Bearer token from [Spotify](https://developer.spotify.com/documentation/general/guides/authorization/scopes/) with [playlist-modify-public](https://developer.spotify.com/documentation/general/guides/authorization/scopes/#playlist-modify-public), [playlist-modify-private](https://developer.spotify.com/documentation/general/guides/authorization/scopes/#playlist-modify-private) scopes |

##### Response headers
| Response header | Value(s) |
| ------------- | ------------- |
| Location  | https://api.spotify.com/v1/playlists/{playlist_id}, where `playlist_id` is the newly created playlist |

##### Example Usage
**Request**
```
POST /v1/playlist/noahteshima/56PBFnmomWOmjg8eZulmMo?size=5 HTTPS/1.1
Host: spotifind-api.com
Authorization: Bearer BQCtdcGa_MtSUA-CSW3HzGjyRHMIXaKzu-pUw8i1_xSJMNgffBaRJA4MQkBDwtOTSNZ-yazOMX8nfhKP-ZE_avChppdubl6k5HfosLHAcrAc6M2HBGZnvG_Ak0VNZU1gch0y9h-IiSjjq12uMpDfsqOlwUkjK25j815P0YddYEY8EacUSHcrNhzCe5aO9w9gMfl0eYnzeniIbASzS4uc8L61aiSRzYe4eIHqbc-vrn6wkQ
```
**Response (201)**

(Note that the response body is intentionally empty.)
```
HTTPS/1.1 201 Created
. . . // Miscellaneous response headers
Location: https://api.spotify.com/v1/playlists/5Rfv2LUBWVu0llq1Oze6yH
. . . // Rest of HTTP message
```

**Request**
```
POST /v1/playlist/noahteshima/invalid_id HTTPS/1.1
Host: spotifind-api.com
Authorization: Bearer BQCtdcGa_MtSUA-CSW3HzGjyRHMIXaKzu-pUw8i1_xSJMNgffBaRJA4MQkBDwtOTSNZ-yazOMX8nfhKP-ZE_avChppdubl6k5HfosLHAcrAc6M2HBGZnvG_Ak0VNZU1gch0y9h-IiSjjq12uMpDfsqOlwUkjK25j815P0YddYEY8EacUSHcrNhzCe5aO9w9gMfl0eYnzeniIbASzS4uc8L61aiSRzYe4eIHqbc-vrn6wkQ
```

**Response (404)**
```
HTTPS/1.1 404 Not Found
. . . // Miscellaneous response headers

{
  "error": {
    "status": 404,
    "message": "Invalid track id."
  }
}
```

**Request**
```
POST /v1/playlist/noahteshima/56PBFnmomWOmjg8eZulmMo HTTPS/1.1
Host: spotifind-api.com
```

**Response (401)**
```
HTTPS/1.1 401 Unauthorized.
. . . // Miscellaneous response headers

{
  "error": {
    "status": 401,
    "message": "Valid authentication credentials not provided."
  }
}
```

**Request**

Suppose `insufficient_token` is a token missing the [playlist-modify-public](https://developer.spotify.com/documentation/general/guides/authorization/scopes/#playlist-modify-public) or [playlist-modify-private](https://developer.spotify.com/documentation/general/guides/authorization/scopes/#playlist-modify-private) scopes.
```
POST /v1/playlist/noahteshima/56PBFnmomWOmjg8eZulmMo HTTPS/1.1
Host: spotifind-api.com
Authorization: Bearer insufficient_token
```

**Response (403)**
```
HTTPS/1.1 403 Forbidden
. . . // Miscellaneous response headers

{
  "error": {
    "status": 403,
    "message": "Insufficient authentication credentials."
  }
}
```

## Contributions
Outside contributions are currently only allowed on an invite-only basis. The following guide is put together to help with onboarding.

### Installation
Spotifind API makes use of the following stack. Feel free to install these with a package manager like [Homebrew](https://brew.sh/).
1. [Python 3.8.x](https://www.python.org/downloads/release/python-380/)
   - [Documentation](https://docs.python.org/3.8/)
2. [Flask 2.1.x](https://flask.palletsprojects.com/en/2.1.x/installation/), our web service framework of choice
   - [Documentation](https://flask.palletsprojects.com/en/2.1.x/#api-reference)
3. Any HTTP service client
   - This project uses [Postman API client](https://www.postman.com/) by default, but [Insomnia](https://insomnia.rest/) is also a good choice that is [directly compatible](https://docs.insomnia.rest/insomnia/import-export-data) with Postman collections.
      - [Postman documentation](https://learning.postman.com/docs/getting-started/introduction/)
4. [Docker](https://docs.docker.com/get-docker/), our container runtime
   - [Quickstart](https://docs.docker.com/get-started/)
   - [Documentation](https://docs.docker.com/reference/)
5. [Kubernetes](https://kubernetes.io/releases/download/), which we use to orchestrate our containerized application
   - [Beginner's guide](https://kubernetes.io/docs/tutorials/kubernetes-basics/)
   - [Documentation](https://kubernetes.io/docs/home/)
6. [Minikube](https://minikube.sigs.k8s.io/docs/start/), which we use for local Kubernetes development
7. [gcloud CLI](https://cloud.google.com/sdk/gcloud), which we use to interface with most resources on [Google Cloud Platform](https://cloud.google.com/) (GCP)
   - Beyond installing the CLI, please email me directly at [noah.teshima@gmail.com](mailto:noah.teshima@gmail.com?subject=GCP%20spotifind%20API%20access) in order to request onboarding to our project on GCP.

### Development

#### Branching strategy
Before making any changes on this project, please make sure to follow the branching strategy established. We currently are unable to set up branch protections since this is a private repository, so good Git hygiene is necessary. For this repository, we use [Github flow](https://docs.github.com/en/get-started/quickstart/github-flow) which is a relatively straightforward branching strategy for new changes we want to introduce on the trunk.

### Making changes

The following is a general strategy that can be adopted when adding new changes during development:
 
1. **Start minikube**. As a quickstart, this part of the documentation can be used to start a [local Kubernetes cluster](https://minikube.sigs.k8s.io/docs/commands/start/). No flags are needed here so the following can be used:
```
minikube start
```
2. **Configure docker-cli to build images directly inside minikube**. This is done so that we can avoid having to push local Docker images to a container registry solely for development. The documentation for [docker-env](https://minikube.sigs.k8s.io/docs/commands/docker-env/) gives additional context; for our use case the following command is sufficient:
```
eval $(minikube docker-env)
```
3. **Configure Kubernetes image pull policy**. The default behavior of our Kubernetes deployments uses an [image pull policy](https://kubernetes.io/docs/concepts/containers/images/#image-pull-policy) of *Always* so that deployments triggered by the CD pipeline adopt the lastest Docker image uploaded to [Google Container Registry](https://cloud.google.com/container-registry). For local development, we don't want this behavior since in the previous step we decided to avoid publishing development images to a container registry. In the Kubernetes resource [file](./deployment.yml), the image and image pull policy for *spotifind-app* should be set as follows:
```
image: spotifind:latest
imagePullPolicy: Never
```
4. **Enable gcp-auth to mount GCP credentials for use on local machine.** [gcp-auth](https://minikube.sigs.k8s.io/docs/handbook/addons/gcp-auth/) is a minikube addon needed to mount GCP credentials onto all Kubernetes pods. Since we use service account keys for machine to machine authentication, this is a necessary step to avoid *4xx* (likely *401*) status codes in development. The following command is sufficient to install the gcp-auth addon:
```
minikube addons enable gcp-auth
```
5. **Enable Ingress for edge routing.** [Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/) is a special type of resource in Kubernetes that we use for load balancing and external access: in other words we need an endpoint to hit from the minikube Kubernetes cluster on our local machine to verify our changes. To do this from minikube, the [ingress-minikube](https://kubernetes.io/docs/tasks/access-application-cluster/ingress-minikube/) addon needs to be installed.
6. **Tunnel with minikube to expose ingress load balancer.** To expose our service from minikube to the operating system on our local machine we use [minikube tunnel](https://minikube.sigs.k8s.io/docs/handbook/accessing/#using-minikube-tunnel). From a separate shell session, the following command needs to execute prior to testing changes:
```
minikube tunnel
```
7. **Run a smoke test.** This is just a shallow but broad test that makes sure the service is running at minimum. We do this to verify the stability of the current build prior to making changes, which is often useful for debugging issues found afterwards. For example, the following endpoint is a health check resource that can be called for this step:
```
GET::127.0.0.1:80/health
```
8. **Build a new Docker image and deploy**. After confirming that minikube is properly running our service, the following shell commands can be used in order to adopt new changes on our service in minikube (this will rebuild the Kubernetes namespace, create a new Docker image with changes, and redeploy changes in minikube):
```
kubectl delete namespace spotifind &&
docker build -t spotifind:latest . &&
kubectl apply -f deployment.yml
```

### Testing

#### Unit testing

For unit tests, we currently run all test suites outside of the Docker container (this is something that can be improved). In order to run a unit test regression, the same command in our [Github workflow](./.github/workflows/ci_pipeline.yml) can be used:
```
python -m unittest discover test/unit_tests/
```

#### Integration testing

Integration tests currently run on the CD, but it is suggested to run integrations tests prior to this to avoid having to revert breaking changes. Since the ANN index service is currently deployed behind a Virtual Private Cloud, all integration tests currently need to be run on a cluster in Google Cloud. To run integration tests, a Kubernetes cluster on [Google Kubernetes Engine](https://cloud.google.com/kubernetes-engine) can be provisioned. From Google Cloud Build, the *GKE-Continuous-Deployment* pipeline can be copied and changed to run on a separate branch. After making these changes, commits added to the remote (this) repository will trigger a new CD pipeline run in Google Cloud.


