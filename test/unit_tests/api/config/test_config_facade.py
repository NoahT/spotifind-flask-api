import unittest
from src.api.config.config_facade import ConfigFacade
import flask

class ConfigFacadeTestSuite(unittest.TestCase):
    def setUp(self) -> None:
        flask_app = flask.Flask(__name__)
        flask_app.config['MATCH_SERVICE_ENABLED'] = True
        flask_app.config['ENVIRONMENT'] = 'development'
        flask_app.config['SPOTIFY_AUTH_CLIENT_CONFIG'] = {
            "CONNECT_TIMEOUT": 0.500,
            "READ_TIMEOUT": 1.000
        }
        flask_app.config['SPOTIFY_CLIENT_CONFIG'] = {
            "CONNECT_TIMEOUT": 0.500,
            "READ_TIMEOUT": 1.000
        }
        with flask_app.app_context():
            self.config_facade = ConfigFacade()

    def test_should_return_environment_when_in_config(self) -> None:
        self.assertEqual('development', self.config_facade.get_environment())

    def test_should_return_if_match_service_client_enabled(self) -> None:
        self.assertTrue(self.config_facade.is_match_service_enabled())
    
    def test_should_return_spotify_auth_client_config(self) -> None:
        spotify_auth_client_config = self.config_facade.get_spotify_auth_client_config()

        self.assertIsNotNone(spotify_auth_client_config)
        self.assertEqual(0.500, spotify_auth_client_config["CONNECT_TIMEOUT"])
        self.assertEqual(1.000, spotify_auth_client_config["READ_TIMEOUT"])
    
    def test_should_return_spotify_auth_client_config(self) -> None:
        spotify_client_config = self.config_facade.get_spotify_client_config()

        self.assertIsNotNone(spotify_client_config)
        self.assertEqual(0.500, spotify_client_config["CONNECT_TIMEOUT"])
        self.assertEqual(1.000, spotify_client_config["READ_TIMEOUT"])