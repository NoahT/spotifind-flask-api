from abc import ABC, abstractmethod
from ..spotify_auth_client.client import SpotifyAuthClient
from ..logging_client.client import LoggingClient
from ...config.config_facade import ConfigFacade
import requests

class Client(ABC):
    @abstractmethod
    def v1_tracks(self, id, marketplace) -> dict:
        pass

    @abstractmethod
    def v1_audio_features(self, id) -> dict:
        pass

class SpotifyClient(Client):
    def __init__(self, auth_client: SpotifyAuthClient, logging_client: LoggingClient, config_facade: ConfigFacade):
        self._hostname = 'https://api.spotify.com'
        self._v1_tracks_path = '/v1/tracks/'
        self._v1_audio_features_path = '/v1/audio-features/'
        self._auth_client = auth_client
        self.logger = logging_client.get_logger(self.__class__.__name__)
        self._config_facade = config_facade

    def v1_tracks(self, id, **kwargs) -> dict:
        batch = self.logger.batch()

        batch.log('Making GET call to /v1/tracks', severity='INFO')
        batch.log('track_id={}'.format(id), severity='INFO')
        endpoint = '{}{}{}'.format(self._hostname, self._v1_tracks_path, id)

        marketplace = kwargs.get('marketplace')

        if marketplace:
            batch.log('marketplace={}'.format(marketplace), severity='INFO')
            endpoint = '{}?market={}'.format(endpoint, marketplace)
        else:
            batch.log('marketplace query param omitted.', severity='INFO')

        bearer_token = self.get_bearer_token()

        headers = {
            'Authorization': bearer_token
        }

        response = requests.get(endpoint, headers=headers, timeout=self.get_timeouts())
        batch.log('status={}'.format(response.status_code), severity='NOTICE')
        response.raise_for_status()
        response_json = response.json()
        batch.log('response={}'.format(response_json), severity='INFO')
        batch.commit()

        return response_json
    
    def v1_audio_features(self, id) -> dict:
        batch = self.logger.batch()

        batch.log('Making GET call to /v1/audio-features', severity='INFO')
        batch.log('track_id={}'.format(id), severity='INFO')
        endpoint = '{}{}{}'.format(self._hostname, self._v1_audio_features_path, id)

        bearer_token = self.get_bearer_token()

        headers = {
            'Authorization': bearer_token
        }

        response = requests.get(endpoint, headers=headers, timeout=self.get_timeouts())
        batch.log('status={}'.format(response.status_code), severity='NOTICE')
        response.raise_for_status()
        response_json = response.json()
        batch.log('response={}'.format(response_json), severity='INFO')
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
        bearer_token = 'Bearer {}'.format(bearer_token)
        
        return bearer_token
