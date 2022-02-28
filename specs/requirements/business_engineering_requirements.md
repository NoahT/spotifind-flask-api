# Business and Engineering Requirements
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
- This is a first iteration of a web service that may change on a contract level, so a gateway should be used here.
  - We might make incompatible changes later. A gateway will help us maintain a looser coupling of components if this happens.
- We cannot rely on bandwidth as a metric for expected traffic since our service's traffic will not have ammortized behavior.
  - Since playlist creation will cause intermittent peak loads for a single host, we should scale horizontally with a balancing strategy that favors inactive nodes.
    - Round robin is usually fine but is not a good balancing strategy here; variable playlist size will not guarantee even distribution of traffic across nodes.
    - We choose least connections as our balancing strategy: nodes with one or more connections is a good indicator for high load and will help us route traffic in a manner compatible with our use case.

## Component Level Design
API design currently focuses on the happy path. Non-200 status codes will be added at a later time for error handling.

### Spotifind Gateway
Our initial design for the gateway will mirror the contract we will uphold in our ReST API.

| Resource  | Description | Type | Parameters |
| ------------- | ------------- | ------------- | ------------- |
| /create/song/{id}?playlistSize={size}  | Retrieve Spotify tracks to recommend based on the given track id | GET | **id** - Spotify Track ID to use when generating playlist <br> **size** - Size of the playlist to generate | 

### Spotifind ReST API

| Resource  | Description | Type | Parameters |
| ------------- | ------------- | ------------- | ------------- |
| /create/song/{id}?playlistSize={size}  | Retrieve Spotify tracks to recommend based on the given track id | GET | **id** - Spotify Track ID to use when generating playlist <br> **size** - Size of the playlist to generate | 

### Spotify APIs (third party)
Spotify's ReST APIs are the only third party APIs being used. Their documentation is sufficient substitution for markdown:
- [Playlist API](https://developer.spotify.com/console/post-playlists/)
- [Tracks API](https://developer.spotify.com/console/get-several-tracks/)
- [Follow API](https://developer.spotify.com/console/put-playlist-followers/)

