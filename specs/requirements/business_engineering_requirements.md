# Business and Engineering Requirements (6/20/22)
We are primarily interested in briefly documenting business and engineering requirements for this web application to constrain our problem space.

## Design Requirements
- Assume all end users have a Spotify account
- Assume fewer than 1000 playlists created per day
- Assume playlist size will be constrained to 50 songs.
- Assume playlist creation has an SLA of 10 seconds end to end.

## Capacity Estimates
- From design requirements, we assume 1000 playlists per day.
  - Song metadata must be passed upstream after using Spotify's bulk API, so we estimate capacity in terms of songs.
    - We empirically estimate 10 KB per song based on experience with Spotify playlists/tracks/follow APIs.
  - 1000 playlists per day, 50 songs for every playlist ~ 5000 songs/day ~ 50000 KB/day ~ 0.5787 KB/sec
    - With buffer, we estimate a bandwidth of 1.5(0.5787 KB/sec) ~ 0.86 KB/sec on average.

## High Level Design
- Recommendations are made on a single song, so a bulk API is not needed.
  - Response time may vary based on the playlist size.
- A gateway is not needed here since we can enforce versioning for our API endpoints for backwards-incompatible changes.
- We use Vertex AI for recommendations for track embeddings.
  - Since Vertex AI offers low-latent recommendations, we will default to round robin for our load balancing strategy.

## Component Level Design
### /v1/reco/{id*}
| Resource  | Description | Type | Parameters |
| ------------- | ------------- | ------------- | ------------- |
| /v1/reco/{id*}  | Retrieve Spotify tracks to recommend based on the given track id | GET | **id** - Spotify Track ID to use when generating playlist <br> **size** - Size of the playlist to generate. Default size 10 | 

#### HTTP response status codes
| Status code | Description |
| ------------- | ------------- |
| 200  | When track id recommendations are returned successfully |
| 400  | Miscellaneous client failure |
| 404  | Client failure due to invalid track id |
| 500  | Miscellaneous service failure |

#### Response headers
| Request header | Value(s) |
| ------------- | ------------- |
| Content-Type  | application/json |

#### Sample requests
**Request**
/v1/reco/62BGM9bNkNcvOh13B4wOyr?size=5

**Response (200)**
```
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
    },
  ]
}
```

**Request**
/v1/reco/invalid_id
**Response (404)**
```
{
  "error": {
    "status": 404,
    "message": "Invalid track id."
  }
}
```

**Request**
/v1/invalid_resource

**Response (404)**
```
{
  "error": {
    "status": 400,
    "message": "Bad request."
  }
}
```

## Spotify APIs (third party)
Spotify's ReST APIs are the only third party APIs being used. Their documentation is sufficient substitution for markdown:
- [Playlist API](https://developer.spotify.com/console/post-playlists/)
- [Tracks API](https://developer.spotify.com/console/get-several-tracks/)
- [Follow API](https://developer.spotify.com/console/put-playlist-followers/)

