""" Unit test module for config_facade. """
import json
import unittest
from unittest.mock import mock_open, patch
from src.api.config.config_facade import ConfigFacade

config = {
    'ENVIRONMENT': 'development',
    'MATCH_SERVICE_ENABLED': False,
    'SPOTIFY_AUTH_CLIENT_CONFIG': {
        'CONNECT_TIMEOUT': 0.500,
        'READ_TIMEOUT': 1.000
    },
    'SPOTIFY_CLIENT_CONFIG': {
        'CONNECT_TIMEOUT': 0.500,
        'READ_TIMEOUT': 0.500
    }
}


# pylint: disable=unused-argument
def env_util_side_effect(*args, **kwargs):
  return 'development'


class ConfigFacadeTestSuite(unittest.TestCase):
  """ Unit test suite for ConfigFacade. """

  def setUp(self) -> None:
    self.config_facade = ConfigFacade()

  @patch('src.api.util.env.env_util')
  @patch('builtins.open', new_callable=mock_open, read_data=json.dumps(config))
  def test_should_return_environment_when_in_config(self, mock_file,
                                                    env_util) -> None:
    env_util.get_environment_variable.side_effect = env_util_side_effect
    self.assertEqual('development', self.config_facade.get_environment())

  @patch('src.api.util.env.env_util')
  @patch('builtins.open', new_callable=mock_open, read_data=json.dumps(config))
  def test_should_return_if_match_service_client_enabled(
      self, mock_file, env_util) -> None:
    env_util.get_environment_variable.side_effect = env_util_side_effect
    self.assertFalse(self.config_facade.is_match_service_enabled())

  @patch('src.api.util.env.env_util')
  @patch('builtins.open', new_callable=mock_open, read_data=json.dumps(config))
  def test_should_return_spotify_auth_client_config(self, mock_file,
                                                    env_util) -> None:
    env_util.get_environment_variable.side_effect = env_util_side_effect
    auth_client_config = self.config_facade.get_spotify_auth_client_config()

    self.assertIsNotNone(auth_client_config)
    self.assertEqual(0.500, auth_client_config['CONNECT_TIMEOUT'])
    self.assertEqual(1.000, auth_client_config['READ_TIMEOUT'])

  @patch('src.api.util.env.env_util')
  @patch('builtins.open', new_callable=mock_open, read_data=json.dumps(config))
  def test_should_return_spotify_client_config(self, mock_file,
                                               env_util) -> None:
    env_util.get_environment_variable.side_effect = env_util_side_effect
    spotify_client_config = self.config_facade.get_spotify_client_config()

    self.assertIsNotNone(spotify_client_config)
    self.assertEqual(0.500, spotify_client_config['CONNECT_TIMEOUT'])
    self.assertEqual(0.500, spotify_client_config['READ_TIMEOUT'])
