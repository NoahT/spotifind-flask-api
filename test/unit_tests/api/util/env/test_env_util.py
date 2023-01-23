import unittest
import src.api.util.env.environment_variable_proxy as environment_variable_proxy
from unittest.mock import patch

class EnvironmentUtilTestSuite(unittest.TestCase):
    def setUp(self) -> None:
        self.env_util = environment_variable_proxy.EnvironmentVariableProxy()
    
    @patch.dict('os.environ', { 'ENVIRONMENT': 'development' })
    def test_should_properly_return_environment_variable_when_available(self) -> None:
        environment = self.env_util.get_environment_variable('ENVIRONMENT')

        self.assertEqual('development', environment)
