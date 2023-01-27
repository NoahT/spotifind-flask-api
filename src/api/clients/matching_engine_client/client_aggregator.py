from . import client
import src.api.config.config_facade as config_facade

class ClientAggregator():
    def __init__(self, config_facade: config_facade.ConfigFacade, mock_match_service_client: client.Client, match_service_client: client.Client) -> None:
        self.config_facade = config_facade
        self.mock_match_service_client = mock_match_service_client
        self.match_service_client = match_service_client
        self.client = None
    
    def get_client(self) -> client.Client:
        if not self.client:
            if self.config_facade.is_match_service_enabled():
                # If we decide to play around with multi-region deployments,
                # this needs to be refactored
                self.client = self.match_service_client(self.config_facade)
            else:
                self.client = self.mock_match_service_client()
            
        return self.client