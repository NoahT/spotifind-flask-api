import unittest
from src.api.clients.matching_engine_client.client import MatchServiceClient
from src.api.config.config_facade import ConfigFacade

class MatchingEngineClientTestSuite(unittest.TestCase):
    def setUp(self) -> None:
        config_facade = ConfigFacade()
        self.match_service_client = MatchServiceClient(config_facade)
    
    def test_should_return_match_response_for_singular_reco(self) -> None:
        match_request = {
            'query': [
                0.762,
                0.213,
                10,
                -14.68,
                1,
                0.128,
                0.52,
                0,
                0.0668,
                0.105
            ],
            'num_recos': 1
        }
        match_response = self.match_service_client.get_match(match_request=match_request)
        self.assertIsNotNone(match_response)
        self.assertEqual(len(match_response), 1)

    def test_should_return_match_response_for_multiple_reco(self) -> None:
        match_request = {
            'query': [
                0.762,
                0.213,
                10,
                -14.68,
                1,
                0.128,
                0.52,
                0,
                0.0668,
                0.105
            ],
            'num_recos': 5
        }
        match_response = self.match_service_client.get_match(match_request=match_request)
        self.assertIsNotNone(match_response)
        self.assertEqual(len(match_response), 5)
