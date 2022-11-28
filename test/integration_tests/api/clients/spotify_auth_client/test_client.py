import unittest
from unittest.mock import Mock
from src.api.clients.spotify_auth_client.client import SpotifyAuthClient
from src.api.clients.logging_client.client import LoggingClient
from requests import HTTPError

class SpotifyClientTestSuite(unittest.TestCase):
    def setUp(self) -> None:
        logging_client = LoggingClient()
        self.auth_client = SpotifyAuthClient(logging_client=logging_client)
    
    def test_should_return_bearer_token_for_valid_basic_authorization(self) -> None:
        bearer_token_dict = self.auth_client.get_bearer_token()
        self.assertIsNotNone(bearer_token_dict)
        self.assertIsNotNone(bearer_token_dict['access_token'])
        self.assertEqual('Bearer', bearer_token_dict['token_type'])
        self.assertIsNotNone(bearer_token_dict['expires_in'])

    def test_should_not_return_bearer_token_for_invalid_basic_authorization(self) -> None:
        self.auth_client.get_basic_token = Mock(return_value='invalid_basic_token')
        self.assertRaises(HTTPError, self.auth_client.get_bearer_token)