from abc import ABC, abstractmethod
from ..spotify_auth_client.client import SpotifyAuthClient

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
        pass

    def get_bearer_token(self) -> str:
        pass
