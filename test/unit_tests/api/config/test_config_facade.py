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


class ConfigFacadeTestSuite(unittest.TestCase):
    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps(config))
    @patch('os.environ', { 'ENVIRONMENT': 'development' })
    def setUp(self, mock_file) -> None:
        self.config_facade = ConfigFacade()
    
    def test_should_return_environment_when_in_config(self) -> None:
        self.assertEqual('development', self.config_facade.get_environment())

    def test_should_return_if_match_service_client_enabled(self) -> None:
        self.assertFalse(self.config_facade.is_match_service_enabled())

    def test_should_return_spotify_auth_client_config(self) -> None:
        spotify_auth_client_config = self.config_facade.get_spotify_auth_client_config()

        self.assertIsNotNone(spotify_auth_client_config)
        self.assertEqual(0.500, spotify_auth_client_config["CONNECT_TIMEOUT"])
        self.assertEqual(1.000, spotify_auth_client_config["READ_TIMEOUT"])

    def test_should_return_spotify_auth_client_config(self) -> None:
        spotify_client_config = self.config_facade.get_spotify_client_config()

        self.assertIsNotNone(spotify_client_config)
        self.assertEqual(0.500, spotify_client_config["CONNECT_TIMEOUT"])
        self.assertEqual(0.500, spotify_client_config["READ_TIMEOUT"])
