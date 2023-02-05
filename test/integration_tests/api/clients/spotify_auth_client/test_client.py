""" Integration test module for Spotify authorization REST API client. """
import unittest
import flask
from unittest.mock import Mock
from src.api.clients.spotify_auth_client.client import SpotifyAuthClient
from src.api.config.config_facade import ConfigFacade
from requests import HTTPError


class SpotifyAuthClientTestSuite(unittest.TestCase):
  """ Integration test suite for SpotifyAuthClient. """

  def setUp(self) -> None:
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
      self.auth_client = SpotifyAuthClient(config_facade=config_facade)

  def test_should_return_bearer_token_for_valid_basic_authorization(
      self) -> None:
    bearer_token_dict = self.auth_client.get_bearer_token()
    self.assertIsNotNone(bearer_token_dict)
    self.assertIsNotNone(bearer_token_dict['access_token'])
    self.assertEqual('Bearer', bearer_token_dict['token_type'])
    self.assertIsNotNone(bearer_token_dict['expires_in'])

  def test_should_not_return_bearer_token_for_invalid_basic_authorization(
      self) -> None:
    self.auth_client.get_basic_token = Mock(return_value='invalid_basic_token')
    self.assertRaises(HTTPError, self.auth_client.get_bearer_token)
