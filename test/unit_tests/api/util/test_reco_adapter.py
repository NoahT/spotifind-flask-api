from unittest.mock import patch
from src.api.util.reco_adapter import V1RecoAdapter
from src.api.clients.matching_engine_client.client_aggregator import ClientAggregator
from src.api.clients.spotify_client.client import SpotifyClient
import unittest

class V1RecoAdapterTestSuite(unittest.TestCase):
    @patch('src.api.clients.matching_engine_client.client_aggregator.ClientAggregator')
    @patch('src.api.clients.spotify_client.client.SpotifyClient')
    def setUp(self, spotify_client, client_aggregator) -> None:
        self.reco_adapter = V1RecoAdapter(spotify_client=spotify_client, client_aggregator=client_aggregator)
    
    def test_should_return_recos_on_happy_path(self) -> None:
        pass

    def test_should_return_404_response_on_invalid_track_id(self) -> None:
        pass

    def test_should_return_400_response_on_invalid_reco_size(self) -> None:
        pass

