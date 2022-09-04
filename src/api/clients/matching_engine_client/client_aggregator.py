from . import client
from ...config.config_facade import ConfigFacade

class ClientAggregator():
    def __init__(self, config_facade: ConfigFacade, mock_match_service_client: client.MockMatchServiceClient, match_service_client: client.MatchServiceClient) -> None:
        self.config_facade = config_facade
        self.mock_match_service_client = mock_match_service_client
        self.match_service_client = match_service_client
    
    def get_client(self) -> client.Client:
        client = self.mock_match_service_client
        if self.config_facade.is_match_service_enabled():
            # If we decide to play around with multi-region deployments,
            # this needs to be refactored
            client = self.match_service_client
        
        return client