import unittest
from src.api.clients.spotify_auth_client.client import SpotifyAuthClient
from src.api.clients.logging_client.client import LoggingClient

class SpotifyClientTestSuite(unittest.TestCase):
    def setUp(self) -> None:
        logging_client = LoggingClient()
        self.auth_client = SpotifyAuthClient(logging_client=logging_client)
    
    def test_should_return_bearer_token_for_valid_basic_authorization(self) -> None:
        pass

    def test_should_not_return_bearer_token_for_invalid_basic_authorization(self) -> None:
        pass