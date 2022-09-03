from unittest.mock import patch
from google.cloud import aiplatform_v1 as aiplatform_v1
import unittest
import src.api.clients.matching_engine_client.client as client

class MockMatchServiceClientTestSuite(unittest.TestCase):
    def setUp(self) -> None:
        self.mock_match_service_client = client.MockMatchServiceClient()

    def test_should_return_response_on_happy_path_for_mock_match_service(self) -> None:
        response = self.mock_match_service_client.get_match(None)
        
        self.assertIsNotNone(response)

        neighbors = response.neighbor
        self.assertEqual(3, len(neighbors))

        neighbor0 = neighbors[0]
        self.assertIsNotNone(neighbor0)
        self.assertIsNotNone(neighbor0.id)
        self.assertIsNotNone(neighbor0.distance)

        neighbor1 = neighbors[1]
        self.assertIsNotNone(neighbor1)
        self.assertIsNotNone(neighbor1.id)
        self.assertIsNotNone(neighbor1.distance)

        neighbor2 = neighbors[2]
        self.assertIsNotNone(neighbor2)
        self.assertIsNotNone(neighbor2.id)
        self.assertIsNotNone(neighbor2.distance)

class MatchServiceClientTestSuite(unittest.TestCase):
    @patch('google.cloud.aiplatform_v1.services.index_endpoint_service.client.IndexEndpointServiceClient')
    @patch('grpc.insecure_channel')
    def setUp(self, channel, index_endpoint_service_client) -> None:
        self.match_service_client = client.MatchServiceClient(location='us-west1', index_endpoint_service_client=index_endpoint_service_client)
        self.match_service_client.DEPLOYED_INDEX_ID = ''

    def test_should_raise_error_on_invalid_query_for_match_service(self) -> None:
        self.assertRaises(KeyError, self.match_service_client.get_match, {})

    def test_should_raise_error_on_empty_query_for_match_service(self) -> None:
        self.assertRaises(ValueError, self.match_service_client.get_match, {'query': []})

    def test_should_return_response_on_happy_path_for_match_service(self) -> None:
        response = self.match_service_client.get_match(match_request={'query': [1, 2, 3]})
        self.assertIsNotNone(response)
