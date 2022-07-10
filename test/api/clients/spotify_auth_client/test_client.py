from unittest.mock import MagicMock, patch
import unittest
import requests
import src.api.clients.spotify_auth_client.client as spotify_auth_client

environment_variables = {
    'PROJECT_ID': '841506577075',
    'CLIENT_ID': '081f994d972f46519c1c8f9f6f11102a',
    'SECRET_ID': 'spotify-rest-api-secret',
    'SECRET_VERSION_ID': 'latest'
}

class SpotifyAuthClientTestSuite(unittest.TestCase):
    @patch.dict('os.environ', environment_variables)
    def setUp(self) -> None:
        self._spotify_auth_client = spotify_auth_client.SpotifyAuthClient()
        self._response = requests.Response()
    
    def test_should_raise_error_for_4xx_response(self):
        self._response.status_code = 400
        requests.post = MagicMock(return_value=self._response)
        self._spotify_auth_client.get_basic_token = MagicMock(return_value='basic_token')

        self.assertRaises(requests.HTTPError, self._spotify_auth_client.get_bearer_token)

    def test_should_raise_error_for_5xx_response(self):
        self._response.status_code = 500
        requests.post = MagicMock(return_value=self._response)
        self._spotify_auth_client.get_basic_token = MagicMock(return_value='basic_token')
        
        self.assertRaises(requests.HTTPError, self._spotify_auth_client.get_bearer_token)

    def test_should_set_correct_headers(self):
        headers = self._spotify_auth_client.get_headers('Bearer basic_auth')

        self.assertEqual(headers, {
            'Authorization': 'Bearer basic_auth',
            'Content-Type': 'application/x-www-form-urlencoded'
        })

    def test_should_set_correct_urlencoded_form(self):
        form_urlencoded = self._spotify_auth_client.get_form_encoded()

        self.assertEqual(form_urlencoded, {
            'grant_type': 'client_credentials'
        })
