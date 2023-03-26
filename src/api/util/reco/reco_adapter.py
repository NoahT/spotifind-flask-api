"""
  Recommendation adapter module. Since the gRPC interface for matching service
  is not directly compatible with our desired API response, we adopt an adapter
  pattern to massage data between both interfaces.
"""
from abc import ABC, abstractmethod
from http import HTTPStatus
from urllib.error import HTTPError
from src.api.clients.spotify_client import SpotifyClient
from src.api.clients.matching_engine_client.client_aggregator import ClientAggregator
from src.api.schemas.response import Response, ResponseBuilderFactory


class RecoAdapter(ABC):
  """
    Adapter class stubs for API response and downstream match service response.
  """

  @abstractmethod
  def get_recos(self,
                track_id: str,
                size: int,
                verbose: bool = False) -> Response:
    pass

  @abstractmethod
  def create_playlist(self, user_id: str, track_id: str, user_token: str,
                      size: str) -> Response:
    pass


class V1RecoAdapter(RecoAdapter):
  """ Adapter class implementation for API response and downstream match service response. """

  def __init__(self, spotify_client: SpotifyClient,
               client_aggregator: ClientAggregator,
               response_builder_factory: ResponseBuilderFactory) -> None:
    self.spotify_client = spotify_client
    self.client_aggregator = client_aggregator
    self._match_service_client = None
    self.response_builder_factory = response_builder_factory
    # This is the feature space we chose for /v1/reco API. Note that these are
    # the same features in Spotify /v1/audio-features API response
    self.feature_mapping = [
        'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
        'acousticness', 'instrumentalness', 'liveness', 'valence'
    ]

  def get_recos(self,
                track_id: str,
                size: str,
                verbose: bool = False) -> Response:
    self.validate_reco_size(size)
    size = int(size)

    audio_features = self.spotify_client.v1_audio_features(track_id=track_id)
    track_embedding = self.get_embedding(audio_features=audio_features)
    recos = self.match_service_client.get_match(match_request={
        'query': track_embedding,
        'num_recos': (size + 1)
    })

    recos_response = recos[0]

    if verbose is True:
      track_ids = [match_neighbor.id for match_neighbor in recos_response]
      v1_tracks_bulk_response = self.spotify_client.v1_tracks_bulk(
          track_ids=track_ids)
      recos_response = v1_tracks_bulk_response['tracks']

    recos_response = self.response_builder_factory.get_builder(
        status_code=HTTPStatus.OK.value).build_response(
            recos_response=recos_response,
            track_id=track_id,
            size=int(size),
            verbose=verbose)

    return recos_response

  def create_playlist(self, user_id: str, track_id: str, user_token: str,
                      size: str) -> Response:
    recos_response = self.get_recos(track_id=track_id, size=size)
    size = int(size)
    recos_response = recos_response.response
    v1_playlist_tracks_payload = self.get_v1_playlist_tracks_payload(
        recos_response=recos_response)

    create_playlist_response = self.spotify_client.v1_create_playlist(
        user_id=user_id, user_token=user_token)
    playlist_id = create_playlist_response['id']

    self.spotify_client.v1_playlist_tracks(playlist_id=playlist_id,
                                           uris=v1_playlist_tracks_payload,
                                           user_token=user_token)

    reco_playlist_response = self.response_builder_factory.get_builder(
        status_code=HTTPStatus.CREATED.value).build_response(
            recos_response={},
            track_id=track_id,
            size=size,
            playlist_id=playlist_id)

    return reco_playlist_response

  def get_v1_playlist_tracks_payload(self, recos_response: dict) -> dict:
    recos_dict = recos_response['recos']
    v1_playlist_tracks_payload = {
        'uris': [f'spotify:track:{reco["id"]}' for reco in recos_dict]
    }

    return v1_playlist_tracks_payload

  def validate_reco_size(self, size: str) -> None:
    if not size.isdigit():
      raise HTTPError(None, HTTPStatus.BAD_REQUEST.value, 'Invalid size type.',
                      None, None)
    if int(size) <= 0:
      raise HTTPError(None, HTTPStatus.BAD_REQUEST.value,
                      'Unable to handle non-positive reco size.', None, None)

  def get_embedding(self, audio_features: dict) -> list:
    embedding = []
    for feature in self.feature_mapping:
      feature_value = audio_features[feature]
      embedding.append(feature_value)

    return embedding

  @property
  def match_service_client(self):
    if not self._match_service_client:
      self._match_service_client = self.client_aggregator.get_client()

    return self._match_service_client
