import unittest
from unittest.mock import Mock
from src.api.clients.spotify_client.client import SpotifyClient
from src.api.clients.spotify_auth_client.client import SpotifyAuthClient
from src.api.clients.logging_client.client import LoggingClient
import requests.exceptions as exceptions

class SpotifyClientTestSuite(unittest.TestCase):
    def setUp(self) -> None:
        logging_client = LoggingClient()
        auth_client = SpotifyAuthClient(logging_client=logging_client)
        self.spotify_client = SpotifyClient(auth_client=auth_client, logging_client=logging_client)
    
    def test_should_return_response_for_valid_track_id(self) -> None:
        response = self.spotify_client.v1_tracks('62BGM9bNkNcvOh13B4wOyr')
        self.assertIsNotNone(response)

    def test_should_return_response_for_valid_track_id_and_marketplace(self) -> None:
        response = self.spotify_client.v1_tracks('62BGM9bNkNcvOh13B4wOyr', marketplace='US')
        self.assertIsNotNone(response)

    def test_should_raise_error_for_invalid_track_id(self) -> None:
        self.assertRaises(exceptions.HTTPError, self.spotify_client.v1_tracks, 'invalid_track_id')

    def test_should_raise_error_for_invalid_bearer_token(self) -> None:
        self.spotify_client.get_bearer_token = Mock(return_value='invalid_bearer_token')
        self.assertRaises(exceptions.HTTPError, self.spotify_client.v1_tracks, '62BGM9bNkNcvOh13B4wOyr')

