# Business and Engineering Requirements (1/28/23)
We are primarily interested in briefly documenting business and engineering requirements for this web application to constrain our problem space.

## Component Level Design
### GET::/v1/reco/{id*}
| Resource       | Description                                                      | Type | Path parameters                                               | Query parameters                                                                                                                                                                                                                                           |
| -------------- | ---------------------------------------------------------------- | ---- | ------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| /v1/reco/{id*} | Retrieve Spotify tracks to recommend based on the given track id | GET  | **id** - Spotify Track ID to use when getting recommendations | **size** - Number of recommendations to return. Default size 5                                                                                                                                                                                             |
|                |                                                                  |      |                                                               | **verbose** - Boolean valued query parameter indicating whether verbose response should be returned for each Spotify track ID. When true, the output for Spotify's `GET::/v1/tracks/{id*}` API is added to each recommended track ID. Default value false. |


#### HTTP response status codes
| Status code | Description                                             |
| ----------- | ------------------------------------------------------- |
| 200         | When track id recommendations are returned successfully |
| 400         | Miscellaneous client failure                            |
| 404         | Client failure due to invalid track id                  |
| 500         | Miscellaneous service failure                           |

#### Response headers
| Request header | Value(s)         |
| -------------- | ---------------- |
| Content-Type   | application/json |

#### Sample requests
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

### POST::/v1/playlist/{user_id*}/{track_id*}
| Resource           | Description                                                                 | Type | Path parameters                                                                                                                                    | Query parameters                                            |
| ------------------ | --------------------------------------------------------------------------- | ---- | -------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------- |
| /v1/playlist/{id*} | Create Spotify playlist with recommended tracks based on the given track id | POST | **user_id** - Spotify user ID to generate the playlist for (i.e. noahteshima) <br> **track_id** - Spotify track ID to use when generating playlist | **size** - Size of the playlist to generate. Default size 5 |

#### HTTP response status codes
| Status code | Description                                                         |
| ----------- | ------------------------------------------------------------------- |
| 201         | When Spotify playlist is created successfully                       |
| 400         | Miscellaneous client failure                                        |
| 401         | Client failure due to missing `Authorization` header                |
| 403         | Client failure due to insufficient scopes in `Authorization` header |
| 404         | Client failure due to invalid track id                              |
| 500         | Miscellaneous service failure                                       |

#### Request headers
| Request header | Value(s)                                                                                                                                                                                                                                                                                                                                                                                                                            |
| -------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Authorization  | Bearer {token}, where `token` is a Bearer token from [Spotify](https://developer.spotify.com/documentation/general/guides/authorization/scopes/) with [playlist-modify-public](https://developer.spotify.com/documentation/general/guides/authorization/scopes/#playlist-modify-public), [playlist-modify-private](https://developer.spotify.com/documentation/general/guides/authorization/scopes/#playlist-modify-private) scopes |

#### Response headers
| Response header | Value(s)                                                                                              |
| --------------- | ----------------------------------------------------------------------------------------------------- |
| Location        | https://api.spotify.com/v1/playlists/{playlist_id}, where `playlist_id` is the newly created playlist |

#### Sample requests
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

## Spotify APIs (third party)
Spotify's REST APIs are the only third party APIs being used. Their documentation is sufficient substitution for markdown:
- [Authorization API](https://developer.spotify.com/documentation/general/guides/authorization/client-credentials/)
- [Audio Features API](https://developer.spotify.com/console/get-audio-features-track/)
- [Create Playlist API](https://developer.spotify.com/console/post-playlists/)
- [Playlist Tracks API](https://developer.spotify.com/console/post-playlist-tracks/)

