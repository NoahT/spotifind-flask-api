import unittest
from src.api.config.config_facade import ConfigFacade
import flask

class ConfigFacadeTestSuite(unittest.TestCase):
    def setUp(self) -> None:
        flask_app = flask.Flask(__name__)
        flask_app.config['MATCH_SERVICE_ENABLED'] = True
        flask_app.config['ENVIRONMENT'] = 'development'
        with flask_app.app_context():
            self.config_facade = ConfigFacade()

    def test_should_return_environment_when_in_config(self) -> None:
        self.assertEquals('development', self.config_facade.get_environment())

    def test_should_return_if_match_service_client_enabled(self) -> None:
        self.assertTrue(self.config_facade.is_match_service_enabled())