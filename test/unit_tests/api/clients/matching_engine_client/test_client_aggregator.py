from unittest.mock import patch
import unittest
from src.api.clients.matching_engine_client.client_aggregator import ClientAggregator

class ClientAggregatorTestSuite(unittest.TestCase):
    @patch('src.api.config.config_facade.ConfigFacade')
    @patch('src.api.clients.matching_engine_client.client.MatchServiceClient')
    @patch('src.api.clients.matching_engine_client.client.MockMatchServiceClient')
    def test_should_return_mock_client_when_match_service_disabled(self, mock_match_service_client, match_service_client, config_facade) -> None:
        config_facade.is_match_service_enabled.return_value = False
        client_aggregator = ClientAggregator(config_facade, mock_match_service_client, match_service_client)
        return_client = client_aggregator.get_client()
        
        self.assertIs(mock_match_service_client, return_client)

    @patch('src.api.config.config_facade.ConfigFacade')
    @patch('src.api.clients.matching_engine_client.client.MatchServiceClient')
    @patch('src.api.clients.matching_engine_client.client.MockMatchServiceClient')
    def test_should_return_match_service_client_when_match_service_enabled(self, mock_match_service_client, match_service_client, config_facade) -> None:
        config_facade.is_match_service_enabled.return_value = True
        client_aggregator = ClientAggregator(config_facade, mock_match_service_client, match_service_client)
        return_client = client_aggregator.get_client()
        
        self.assertIs(match_service_client, return_client)
