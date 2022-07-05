from unittest.mock import MagicMock, patch
import unittest
import src.api.clients.spotify_client.client as spotify_client
import src.api.clients.spotify_auth_client.client as spotify_auth_client

environment_variables = {
    'PROJECT_ID': '841506577075',
    'CLIENT_ID': '081f994d972f46519c1c8f9f6f11102a',
    'SECRET_ID': 'spotify-rest-api-secret',
    'SECRET_VERSION_ID': 'latest'
}

class SpotifyClientTestSuite(unittest.TestCase):
    @patch.dict('os.environ', environment_variables)
    def setUp(self) -> None:
        self._spotify_client = spotify_client.SpotifyClient()
    
    def test_should_raise_error_for_4xx_response(self):
        pass

    def test_should_raise_error_for_5xx_response(self):
        pass

    def test_should_return_json_for_2xx_response(self):
        pass

    def test_should_return_correct_authorization_header(self):
        pass
