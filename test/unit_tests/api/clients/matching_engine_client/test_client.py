""" Unit test module for matching engine client. """
from unittest.mock import patch
import unittest
from src.api.clients.matching_engine_client.client import MockMatchServiceClient, MatchServiceClient


class MockMatchServiceClientTestSuite(unittest.TestCase):
  """ Unit test suite for MockMatchServiceClient. """

  def setUp(self) -> None:
    self.mock_match_service_client = MockMatchServiceClient()

  def test_should_return_response_on_happy_path_for_mock_match_service(
      self) -> None:
    response = self.mock_match_service_client.get_match(None)
    self.assertIsNotNone(response)
    self.assertEqual(1, len(response))

    response0 = response[0]
    self.assertIsNotNone(response0)
    self.assertEqual(3, len(response0))

    neighbor0 = response0[0]
    self.assertIsNotNone(neighbor0)
    self.assertIsNotNone(neighbor0.id)
    self.assertIsNotNone(neighbor0.distance)

    neighbor1 = response0[1]
    self.assertIsNotNone(neighbor1)
    self.assertIsNotNone(neighbor1.id)
    self.assertIsNotNone(neighbor1.distance)

    neighbor2 = response0[2]
    self.assertIsNotNone(neighbor2)
    self.assertIsNotNone(neighbor2.id)
    self.assertIsNotNone(neighbor2.distance)


class MatchServiceClientTestSuite(unittest.TestCase):
  """ Unit test suite for MatchServiceClient. """

  @patch('src.api.util.env.env_util')
  @patch('src.api.config.config_facade')
  @patch('google.cloud.aiplatform.MatchingEngineIndexEndpoint')
  # pylint: disable=unused-argument
  def setUp(self, matching_engine_index_endpoint, config_facade,
            env_util) -> None:
    env_util.get_environment_variable.return_value = 'mock_env'
    self.match_service_client = MatchServiceClient(config_facade)
    self.match_service_client.DEPLOYED_INDEX_ID = ''

  def test_should_raise_error_on_invalid_query_for_match_service(self) -> None:
    self.assertRaises(KeyError, self.match_service_client.get_match, {})

  def test_should_raise_error_on_empty_query_for_match_service(self) -> None:
    self.assertRaises(ValueError, self.match_service_client.get_match, {
        'query': [],
        'num_recos': 5
    })

  def test_should_return_response_on_happy_path_for_match_service(self) -> None:
    response = self.match_service_client.get_match(match_request={
        'query': [1, 2, 3],
        'num_recos': 5
    })
    self.assertIsNotNone(response)
