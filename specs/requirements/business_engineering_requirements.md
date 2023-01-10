# Business and Engineering Requirements (1/10/23)
We are primarily interested in briefly documenting business and engineering requirements for this web application to constrain our problem space.

## Component Level Design
### GET::/v1/reco/{id*}
| Resource  | Description | Type | Parameters |
| ------------- | ------------- | ------------- | ------------- |
| /v1/reco/{id*}  | Retrieve Spotify tracks to recommend based on the given track id | GET | **id** - Spotify Track ID to use when getting recommendations <br> **size** - Number of recommendations to return. Default size 5 | 

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
    }
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

### POST::/v1/playlist/{id*}
| Resource  | Description | Type | Parameters |
| ------------- | ------------- | ------------- | ------------- |
| /v1/playlist/{id*}  | Create Spotify playlist with recommended tracks based on the given track id | POST | **id** - Spotify Track ID to use when generating playlist <br> **size** - Size of the playlist to generate. Default size 5 | 

#### HTTP response status codes
| Status code | Description |
| ------------- | ------------- |
| 201  | When Spotify playlist is created successfully |
| 400  | Miscellaneous client failure |
| 401  | Client failure due to missing `Authorization` header |
| 403  | Client failure due to insufficient scopes in `Authorization` header |
| 404  | Client failure due to invalid track id |
| 500  | Miscellaneous service failure |

#### Request headers
| Request header | Value(s) |
| ------------- | ------------- |
| Authorization  | Bearer {token}, where `token` is a Bearer token from [Spotify](https://developer.spotify.com/documentation/general/guides/authorization/scopes/) with [playlist-modify-public](https://developer.spotify.com/documentation/general/guides/authorization/scopes/#playlist-modify-public), [playlist-modify-private](https://developer.spotify.com/documentation/general/guides/authorization/scopes/#playlist-modify-private) scopes |

#### Response headers
| Request header | Value(s) |
| ------------- | ------------- |
| Location  | https://api.spotify.com/v1/playlists/{playlist_id}, where `playlist_id` is the newly created playlist |

#### Sample requests
**Request**
/v1/reco/62BGM9bNkNcvOh13B4wOyr?size=5

**Response (201)**

(Note that the response body is intentionally empty.)
```
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
Spotify's REST APIs are the only third party APIs being used. Their documentation is sufficient substitution for markdown:
- [Authorization API](https://developer.spotify.com/documentation/general/guides/authorization/client-credentials/)
- [Audio Features API](https://developer.spotify.com/console/get-audio-features-track/)
- [Create Playlist API](https://developer.spotify.com/console/post-playlists/)
- [Playlist Tracks API](https://developer.spotify.com/console/post-playlist-tracks/)

