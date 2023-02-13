""" Integration test module for Spotify REST API client. """
import unittest
import flask
from unittest.mock import Mock
from src.api.clients.spotify_client.client import SpotifyClient
from src.api.clients.spotify_auth_client.client import SpotifyAuthClient
from src.api.clients.logging_client.client import LoggingClient
from src.api.config.config_facade import ConfigFacade
from requests import exceptions


class SpotifyClientTestSuite(unittest.TestCase):
  """ Integration test suite for SpotifyClient. """

  def setUp(self) -> None:
    logging_client = LoggingClient()

    flask_app = flask.Flask(__name__)
    flask_app.config['MATCH_SERVICE_ENABLED'] = True
    flask_app.config['ENVIRONMENT'] = 'staging'
    flask_app.config['SPOTIFY_AUTH_CLIENT_CONFIG'] = {
        'CONNECT_TIMEOUT': 0.500,
        'READ_TIMEOUT': 1.000
    }
    flask_app.config['SPOTIFY_CLIENT_CONFIG'] = {
        'CONNECT_TIMEOUT': 0.500,
        'READ_TIMEOUT': 1.000
    }
    with flask_app.app_context():
      config_facade = ConfigFacade()
      auth_client = SpotifyAuthClient(config_facade=config_facade)
      self._spotify_client = SpotifyClient(auth_client=auth_client,
                                           logging_client=logging_client,
                                           config_facade=config_facade)
      self._auth_client = auth_client

  def test_should_return_response_for_valid_track_id_on_v1_tracks(self) -> None:
    response = self._spotify_client.v1_tracks('62BGM9bNkNcvOh13B4wOyr')
    self.assertIsNotNone(response)

  # pylint: disable-next=line-too-long
  def test_should_return_response_for_valid_track_id_and_marketplace_on_v1_tracks(
      self) -> None:
    response = self._spotify_client.v1_tracks('62BGM9bNkNcvOh13B4wOyr',
                                              marketplace='US')
    self.assertIsNotNone(response)

  def test_should_raise_error_for_invalid_track_id_on_v1_tracks(self) -> None:
    self.assertRaises(exceptions.HTTPError, self._spotify_client.v1_tracks,
                      'invalid_track_id')

  def test_should_raise_error_for_invalid_bearer_token_on_v1_tracks(
      self) -> None:
    self._spotify_client.get_bearer_token = Mock(
        return_value='invalid_bearer_token')
    self.assertRaises(exceptions.HTTPError, self._spotify_client.v1_tracks,
                      '62BGM9bNkNcvOh13B4wOyr')

  def test_should_return_response_for_valid_track_id_on_v1_audio_features(
      self) -> None:
    response = self._spotify_client.v1_audio_features('62BGM9bNkNcvOh13B4wOyr')
    self.assertIsNotNone(response)
    self.assertIsNotNone(response['danceability'])
    self.assertIsNotNone(response['energy'])
    self.assertIsNotNone(response['key'])
    self.assertIsNotNone(response['loudness'])
    self.assertIsNotNone(response['mode'])
    self.assertIsNotNone(response['speechiness'])
    self.assertIsNotNone(response['acousticness'])
    self.assertIsNotNone(response['instrumentalness'])
    self.assertIsNotNone(response['liveness'])
    self.assertIsNotNone(response['valence'])
    self.assertIsNotNone(response['tempo'])

  def test_should_raise_error_for_invalid_track_id_on_v1_audio_features(
      self) -> None:
    self.assertRaises(exceptions.HTTPError,
                      self._spotify_client.v1_audio_features,
                      'invalid_track_id')

  def test_should_raise_error_for_invalid_bearer_token_on_v1_audio_features(
      self) -> None:
    self._spotify_client.get_bearer_token = Mock(
        return_value='invalid_bearer_token')
    self.assertRaises(exceptions.HTTPError,
                      self._spotify_client.v1_audio_features,
                      '62BGM9bNkNcvOh13B4wOyr')

  def test_should_raise_error_for_invalid_bearer_token_on_v1_create_playlist(
      self) -> None:
    self.assertRaises(exceptions.HTTPError,
                      self._spotify_client.v1_create_playlist, 'noahteshima',
                      'invalid_token')

  def test_should_raise_error_for_wrong_token_scope_on_v1_create_playlist(
      self) -> None:
    # public, read-only scope - will cause 403 due to insufficient permission
    token = self._auth_client.get_bearer_token()
    token = f'Bearer {token}'
    self.assertRaises(exceptions.HTTPError,
                      self._spotify_client.v1_create_playlist, 'noahteshima',
                      token)

  def test_should_raise_error_for_invalid_bearer_token_on_v1_playlist_tracks(
      self) -> None:
    pass

  def test_should_raise_error_for_wrong_token_scope_on_v1_playlist_tracks(
      self) -> None:
    pass
