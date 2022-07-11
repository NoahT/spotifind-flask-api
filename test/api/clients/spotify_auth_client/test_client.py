from unittest.mock import MagicMock, patch
import unittest
import requests
import src.api.clients.spotify_auth_client.client as spotify_auth_client

environment_variables = {
    'PROJECT_ID': '841506577075',
    'CLIENT_ID': '081f994d972f46519c1c8f9f6f11102a',
    'SECRET_ID': 'spotify-rest-api-secret',
    'SECRET_VERSION_ID': 'latest',
    'PROJECT_NAME': 'spotifind-api'
}

class SpotifyAuthClientTestSuite(unittest.TestCase):
    @patch.dict('os.environ', environment_variables)
    @patch('src.api.clients.logging_client.client.LoggingClient')
    def setUp(self, logging_client) -> None:
        self._spotify_auth_client = spotify_auth_client.SpotifyAuthClient()
        self._response = requests.Response()
    
    @patch('src.api.clients.logging_client.client.LoggingClient')
    def test_should_raise_error_for_4xx_response(self, logging_client):
        self._response.status_code = 400
        requests.post = MagicMock(return_value=self._response)
        self._spotify_auth_client.get_basic_token = MagicMock(return_value='basic_token')

        self.assertRaises(requests.HTTPError, self._spotify_auth_client.get_bearer_token)

    @patch('src.api.clients.logging_client.client.LoggingClient')
    def test_should_raise_error_for_5xx_response(self, logging_client):
        self._response.status_code = 500
        requests.post = MagicMock(return_value=self._response)
        self._spotify_auth_client.get_basic_token = MagicMock(return_value='basic_token')
        
        self.assertRaises(requests.HTTPError, self._spotify_auth_client.get_bearer_token)

    @patch('src.api.clients.logging_client.client.LoggingClient')
    def test_should_set_correct_headers(self, logging_client):
        headers = self._spotify_auth_client.get_headers('Bearer basic_auth')

        self.assertEqual(headers, {
            'Authorization': 'Bearer basic_auth',
            'Content-Type': 'application/x-www-form-urlencoded'
        })

    @patch('src.api.clients.logging_client.client.LoggingClient')
    def test_should_set_correct_urlencoded_form(self, logging_client):
        form_urlencoded = self._spotify_auth_client.get_form_encoded()

        self.assertEqual(form_urlencoded, {
            'grant_type': 'client_credentials'
        })
