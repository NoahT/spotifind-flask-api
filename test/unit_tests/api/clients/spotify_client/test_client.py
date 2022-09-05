from unittest.mock import Mock, patch
import unittest
import src.api.clients.spotify_client.client as spotify_client
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
        logging_client = Mock()
        auth_client = Mock()
        self._spotify_client = spotify_client.SpotifyClient(auth_client, logging_client)
        self._response = requests.Response()
    
    def test_should_raise_error_for_4xx_response_on_v1_tracks(self):
        self._response.status_code = 400
        requests.get = Mock(return_value=self._response)
        self._spotify_client.get_bearer_token = Mock(return_value='Bearer token')

        self.assertRaises(requests.HTTPError, self._spotify_client.v1_tracks, 'id')

    def test_should_raise_error_for_5xx_response_on_v1_tracks(self):
        self._response.status_code = 500
        requests.get = Mock(return_value=self._response)
        self._spotify_client.get_bearer_token = Mock(return_value='Bearer token')

        self.assertRaises(requests.HTTPError, self._spotify_client.v1_tracks, 'id')

    def test_should_return_json_for_2xx_response_on_v1_tracks(self):
        self._response.status_code = 200
        requests.get = Mock(return_value=self._response)
        requests.Response.json = Mock(return_value={})
        self._spotify_client.get_bearer_token = Mock(return_value='Bearer token')

        response = self._spotify_client.v1_tracks('id')

        self.assertEqual({}, response)
    
    def test_should_raise_error_for_4xx_response_on_v1_audio_features(self):
        self._response.status_code = 400
        requests.get = Mock(return_value=self._response)
        self._spotify_client.get_bearer_token = Mock(return_value='Bearer token')

        self.assertRaises(requests.HTTPError, self._spotify_client.v1_audio_features, 'id')

    def test_should_raise_error_for_5xx_response_on_v1_audio_features(self):
        self._response.status_code = 500
        requests.get = Mock(return_value=self._response)
        self._spotify_client.get_bearer_token = Mock(return_value='Bearer token')

        self.assertRaises(requests.HTTPError, self._spotify_client.v1_audio_features, 'id')

    def test_should_return_json_for_2xx_response_on_v1_audio_features(self):
        self._response.status_code = 200
        requests.get = Mock(return_value=self._response)
        requests.Response.json = Mock(return_value={})
        self._spotify_client.get_bearer_token = Mock(return_value='Bearer token')

        response = self._spotify_client.v1_audio_features('id')

        self.assertEqual({}, response)

    def test_should_return_correct_authorization_header(self):
        auth_client = Mock()
        auth_client.get_bearer_token.return_value = {
            'access_token': 'token'
        }
        logging_client = Mock()
        self._spotify_client = spotify_client.SpotifyClient(auth_client, logging_client)

        bearer_token = self._spotify_client.get_bearer_token()

        self.assertEqual('Bearer token', bearer_token)
