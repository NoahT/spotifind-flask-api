""" Spotify REST API client module. """
from abc import ABC, abstractmethod
from google.cloud import logging_v2
from src.api.clients.spotify_auth_client import SpotifyAuthClient
from src.api.clients.logging_client import LoggingClient
from src.api.config.config_facade import ConfigFacade
import json
import requests


class Client(ABC):
  """ Abstract base class for Spotify API client. """

  @abstractmethod
  def v1_tracks(self, track_id: str, marketplace: str) -> dict:
    pass

  @abstractmethod
  def v1_tracks_bulk(self, track_ids: list, marketplace: str) -> dict:
    pass

  @abstractmethod
  def v1_audio_features(self, track_id: str) -> dict:
    pass

  @abstractmethod
  def v1_create_playlist(
      self,
      user_id,
      user_token,
      name='Spotifind playlist',
      description='https://github.com/NoahT/spotifind-flask-api',
      is_public=True) -> dict:
    pass

  @abstractmethod
  def v1_playlist_tracks(self, playlist_id: str, uris: dict,
                         user_token: str) -> dict:
    pass


class SpotifyClient(Client):
  """ Spotify REST API client implementation. """

  def __init__(self, auth_client: SpotifyAuthClient,
               logging_client: LoggingClient, config_facade: ConfigFacade):
    self._hostname = 'https://api.spotify.com'
    self._v1_tracks_path = '/v1/tracks/'
    self._v1_tracks_bulk_path = '/v1/tracks'
    self._v1_audio_features_path = '/v1/audio-features/'
    self._v1_create_playlist_path = '/v1/users/{}/playlists'
    self._v1_playlist_tracks_path = '/v1/playlists/{}/tracks'
    self._auth_client = auth_client
    self._logging_client = logging_client
    self._logger = None
    self._config_facade = config_facade

  def v1_tracks(self, track_id: str, **kwargs) -> dict:
    batch = self.logger.batch()

    batch.log(f'Making GET call to {self._v1_tracks_path}', severity='INFO')
    batch.log(f'track_id={track_id}', severity='INFO')
    url = f'{self._hostname}{self._v1_tracks_path}{track_id}'

    marketplace = kwargs.get('marketplace')

    if marketplace:
      batch.log(f'marketplace={marketplace}', severity='INFO')
      url = f'{url}?market={marketplace}'
    else:
      batch.log('marketplace query param omitted.', severity='INFO')

    bearer_token = self.get_bearer_token()

    headers = {'Authorization': bearer_token}

    response = requests.get(url, headers=headers, timeout=self.get_timeouts())
    batch.log(f'status={response.status_code}', severity='NOTICE')
    response.raise_for_status()
    response_json = response.json()
    batch.log(f'response={response_json}', severity='INFO')
    batch.commit()

    return response_json

  def v1_tracks_bulk(self, track_ids: list, **kwargs) -> dict:
    batch = self.logger.batch()

    batch.log(f'Making GET call to {self._v1_tracks_bulk_path}',
              severity='INFO')

    track_ids_string = ','.join(track_ids)
    batch.log(f'track_ids={track_ids_string}', severity='INFO')
    url = f'{self._hostname}{self._v1_tracks_bulk_path}?ids={track_ids_string}'

    marketplace = kwargs.get('marketplace')

    if marketplace:
      batch.log(f'marketplace={marketplace}', severity='INFO')
      url = f'{url}?market={marketplace}'
    else:
      batch.log('marketplace query param omitted.', severity='INFO')

    bearer_token = self.get_bearer_token()

    headers = {'Authorization': bearer_token}

    response = requests.get(url=url,
                            headers=headers,
                            timeout=self.get_timeouts())
    batch.log(f'status={response.status_code}', severity='NOTICE')
    response.raise_for_status()
    response_json = response.json()
    batch.log(f'response={response_json}', severity='INFO')
    batch.commit()

    return response_json

  def v1_audio_features(self, track_id: str) -> dict:
    batch = self.logger.batch()

    batch.log(f'Making GET call to {self._v1_audio_features_path}',
              severity='INFO')
    batch.log(f'track_id={track_id}', severity='INFO')
    url = f'{self._hostname}{self._v1_audio_features_path}{track_id}'

    bearer_token = self.get_bearer_token()

    headers = {'Authorization': bearer_token}

    response = requests.get(url, headers=headers, timeout=self.get_timeouts())
    batch.log(f'status={response.status_code}', severity='NOTICE')
    response.raise_for_status()
    response_json = response.json()
    batch.log(f'response={response_json}', severity='INFO')
    batch.commit()

    return response_json

  def v1_create_playlist(
      self,
      user_id,
      user_token,
      name='Spotifind playlist',
      description='https://github.com/NoahT/spotifind-flask-api',
      is_public=True) -> dict:
    batch = self.logger.batch()

    playlist_resource = self._v1_create_playlist_path.format(user_id)
    url = f'{self._hostname}{playlist_resource}'

    batch.log(f'Making POST call to {playlist_resource}', severity='INFO')
    batch.log(f'user_id={user_id}', severity='INFO')

    payload = {'name': name, 'description': description, 'public': is_public}
    batch.log(f'payload={json.dumps(payload)}', severity='INFO')

    headers = {'Authorization': user_token}

    response = requests.post(url,
                             headers=headers,
                             timeout=self.get_timeouts(),
                             json=json.loads(json.dumps(payload)))
    batch.log(f'status={response.status_code}', severity='NOTICE')
    response.raise_for_status()
    response_json = response.json()
    batch.log(f'response={response_json}', severity='INFO')
    batch.commit()

    return response_json

  def v1_playlist_tracks(self, playlist_id: str, uris: dict,
                         user_token: str) -> dict:
    batch = self.logger.batch()

    playlist_resource = self._v1_playlist_tracks_path.format(playlist_id)
    url = f'{self._hostname}{playlist_resource}'

    batch.log(f'Making POST call to {playlist_resource}', severity='INFO')
    batch.log(f'playlist_id={playlist_id}', severity='INFO')

    batch.log(f'payload={json.dumps(uris)}', severity='INFO')

    headers = {'Authorization': user_token}

    response = requests.post(url=url,
                             json=json.loads(json.dumps(uris)),
                             headers=headers,
                             timeout=self.get_timeouts())
    batch.log(f'status={response.status_code}', severity='NOTICE')
    response.raise_for_status()
    response_json = response.json()
    batch.log(f'response={json.dumps(response_json)}', severity='INFO')
    batch.commit()

    return response_json

  def get_timeouts(self) -> tuple:
    spotify_client_config = self._config_facade.get_spotify_client_config()
    read_timeout = spotify_client_config['READ_TIMEOUT']
    connect_timeout = spotify_client_config['CONNECT_TIMEOUT']

    return (connect_timeout, read_timeout)

  def get_bearer_token(self) -> str:
    bearer_token_json = self._auth_client.get_bearer_token()

    bearer_token = bearer_token_json['access_token']
    bearer_token = f'Bearer {bearer_token}'

    return bearer_token

  @property
  def logger(self) -> logging_v2.Logger:
    if not self._logger:
      self._logger = self._logging_client.get_logger(self.__class__.__name__)

    return self._logger
