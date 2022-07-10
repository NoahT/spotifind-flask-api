from unittest.mock import MagicMock, patch
import unittest
import src.api.clients.logging_client.client as logging_client

environment_variables={
    'PROJECT_NAME': 'spotifind-api'
}

class LoggingClientSuite(unittest.TestCase):
    @patch.dict('os.environ', environment_variables)
    def setUp(self) -> None:
        self.client = logging_client.LoggingClient()

    def test_should_properly_initialize_logging_client_on_creation(self) -> None:
        project = self.client.client.project
        self.assertEquals(project, 'spotifind-api')

    def test_should_return_logger_from_logging_client_from_given_name(self) -> None:
        logger = self.client.get_logger('name')
        self.assertEquals(logger.name, 'name')
