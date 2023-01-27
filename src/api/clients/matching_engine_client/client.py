from abc import ABC, abstractmethod
from google.cloud import aiplatform
from google.cloud.aiplatform.matching_engine.matching_engine_index_endpoint import MatchNeighbor
import src.api.config.config_facade as config_facade
import src.api.util.env as env

REGION_DEFAULT = 'us-west1'
LOCATION_URI = 'projects/{}/locations/{}'
AIPLATFORM_ENDPOINT_URI = '{}-aiplatform.googleapis.com'

class Client(ABC):
    @abstractmethod
    def get_match(self, match_request: dict) -> list:
        pass

class MockMatchServiceClient(Client):
    def get_match(self, match_request: dict) -> list:
        response = []
        
        neighbor1 = MatchNeighbor('7C48cUjCGx14K5b41e9vTD', 1)
        neighbor2 = MatchNeighbor('3x7gMvCsL1SS6THGwB55Pm', 2)
        neighbor3 = MatchNeighbor('7sLQGgXFs4LaGAaDErPwOl', 5)

        response.extend([neighbor1, neighbor2, neighbor3])

        return response

class MatchServiceClient(Client):
    def __init__(self, config_facade: config_facade.ConfigFacade) -> None:
        self._region = env.env_util.get_environment_variable('REGION', default=REGION_DEFAULT)
        self._environment = env.env_util.get_environment_variable('ENVIRONMENT')
        self._project_id = env.env_util.get_environment_variable('PROJECT_ID')
        self._location = LOCATION_URI.format(self._project_id, self._region)
        self._config_facade = config_facade
        
        self.get_service_metadata()
    
    def get_match(self, match_request: dict) -> list:
        query = match_request['query']
        if len(query) == 0:
            raise ValueError('Empty query provided.')
        
        num_recos = match_request['num_recos']
        
        match_neighbors = self._index_endpoint.match(
            deployed_index_id=self._deployed_index_id,
            queries=[query],
            num_neighbors=num_recos
        )
        
        return match_neighbors
    
    def get_service_metadata(self) -> None:
        index_endpoint = aiplatform.MatchingEngineIndexEndpoint.list(
            filter='labels.environment={} AND labels.region={}'.format(self._environment, self._region),
            project=self._project_id,
            location=self._region
        )[0]
        self._deployed_index_id = index_endpoint.deployed_indexes[0].id

        self._index_endpoint = index_endpoint
