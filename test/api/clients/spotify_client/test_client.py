from unittest.mock import MagicMock, patch
import unittest
import src.api.clients.spotify_client.client as spotify_client
import src.api.clients.spotify_auth_client.client as spotify_auth_client
import requests

environment_variables = {
    'PROJECT_ID': '841506577075',
    'CLIENT_ID': '081f994d972f46519c1c8f9f6f11102a',
    'SECRET_ID': 'spotify-rest-api-secret',
    'SECRET_VERSION_ID': 'latest',
    'PROJECT_NAME': 'spotifind-api'
}

class SpotifyClientTestSuite(unittest.TestCase):
    @patch.dict('os.environ', environment_variables)
    def setUp(self) -> None:
        self._spotify_client = spotify_client.SpotifyClient()
        self._response = requests.Response()
    
    def test_should_raise_error_for_4xx_response(self):
        self._response.status_code = 400
        requests.get = MagicMock(return_value=self._response)
        self._spotify_client.get_bearer_token = MagicMock(return_value='Bearer token')

        self.assertRaises(requests.HTTPError, self._spotify_client.v1_tracks, 'id')

    def test_should_raise_error_for_5xx_response(self):
        self._response.status_code = 500
        requests.get = MagicMock(return_value=self._response)
        self._spotify_client.get_bearer_token = MagicMock(return_value='Bearer token')

        self.assertRaises(requests.HTTPError, self._spotify_client.v1_tracks, 'id')

    def test_should_return_json_for_2xx_response(self):
        self._response.status_code = 200
        requests.get = MagicMock(return_value=self._response)
        requests.Response.json = MagicMock(return_value={})
        self._spotify_client.get_bearer_token = MagicMock(return_value='Bearer token')

        response = self._spotify_client.v1_tracks('id')

        self.assertEqual({}, response)

    def test_should_return_correct_authorization_header(self):
        spotify_auth_client.SpotifyAuthClient.get_bearer_token = MagicMock(return_value={
            'access_token': 'token'
        })

        bearer_token = self._spotify_client.get_bearer_token()

        self.assertEqual('Bearer token', bearer_token)
