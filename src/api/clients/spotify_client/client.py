from abc import ABC, abstractmethod
from ..spotify_auth_client.client import SpotifyAuthClient
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

    def v1_tracks(self, id, marketplace) -> dict:
        endpoint = '{}{}{}'.format(self._hostname, self._v1_tracks_path, id)

        if marketplace:
            endpoint = '{}?market={}'.format(endpoint, marketplace)

        bearer_token = self.get_bearer_token()

        headers = {
            'Authorization': bearer_token
        }

        response = requests.get(endpoint, headers=headers)
        response.raise_for_status()
        response_json = response.json()

        return response_json
    
    def get_bearer_token(self) -> str:
        bearer_token_json = self._auth_client.get_bearer_token()

        bearer_token = bearer_token_json['access_token']
        bearer_token = 'Bearer {}'.format(bearer_token)
        
        return bearer_token
