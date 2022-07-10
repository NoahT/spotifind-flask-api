from abc import ABC, abstractmethod
from ..spotify_auth_client.client import SpotifyAuthClient
from ..logging_client.client import LoggingClient
import requests

class Client(ABC):
    @abstractmethod
    def v1_tracks(self, id, marketplace) -> dict:
        pass

class SpotifyClient(Client):
    def __init__(self):
        self._auth_client = SpotifyAuthClient()
        self._hostname = 'https://api.spotify.com'
        self._v1_tracks_path = '/v1/tracks/'
        logging_client = LoggingClient()
        self.logger = logging_client.get_logger(self.__class__.__name__)

    def v1_tracks(self, id, **kwargs) -> dict:
        batch = self.logger.batch()

        batch.log('Making GET call to /v1/tracks', severity='INFO')
        batch.log('track_id={}'.format(id), severity='INFO')
        endpoint = '{}{}{}'.format(self._hostname, self._v1_tracks_path, id)

        marketplace = kwargs.get('marketplace')

        if marketplace:
            batch.log('marketplace={}'.format(marketplace), severity='INFO')
            endpoint = '{}?market={}'.format(endpoint, marketplace)

        bearer_token = self.get_bearer_token()

        headers = {
            'Authorization': bearer_token
        }

        response = requests.get(endpoint, headers=headers)
        batch.commit()
        response.raise_for_status()
        response_json = response.json()

        return response_json
    
    def get_bearer_token(self) -> str:
        bearer_token_json = self._auth_client.get_bearer_token()

        bearer_token = bearer_token_json['access_token']
        bearer_token = 'Bearer {}'.format(bearer_token)
        
        return bearer_token
