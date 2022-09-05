from abc import ABC, abstractmethod
from ..clients.spotify_client.client import SpotifyClient
from ..clients.matching_engine_client.client_aggregator import ClientAggregator

class RecoAdapter(ABC):
    @abstractmethod
    def get_recos(id: str, size: int) -> dict:
        pass

class V1RecoAdapter(RecoAdapter):
    def __init__(self, spotify_client: SpotifyClient, client_aggregator: ClientAggregator) -> None:
        self.spotify_client = spotify_client
        self.client_aggregator = client_aggregator
    
    def get_recos(self, id: str, size: int) -> dict:
        return {}
    