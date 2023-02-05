"""
  Matching engine gRPC client module.
  e 23/2/5: We no longer maintain the .proto files and generated code. This
  responsibility is shifted to the google cloud aiplatform libraries in the
  latest version.
"""
from abc import ABC, abstractmethod
from google.cloud import aiplatform
from google.cloud.aiplatform.matching_engine.matching_engine_index_endpoint import MatchNeighbor
from src.api.config.config_facade import ConfigFacade
from src.api.util import env

REGION_DEFAULT = 'us-west1'
LOCATION_URI = 'projects/{}/locations/{}'
AIPLATFORM_ENDPOINT_URI = '{}-aiplatform.googleapis.com'


class Client(ABC):
  """ Abstract base class for matching engine client. """

  @abstractmethod
  def get_match(self, match_request: dict) -> list:
    pass


class MockMatchServiceClient(Client):
  """ Mock match service implementation. """

  def get_match(self, match_request: dict) -> list:
    response = []

    neighbor1 = MatchNeighbor('7C48cUjCGx14K5b41e9vTD', 1)
    neighbor2 = MatchNeighbor('3x7gMvCsL1SS6THGwB55Pm', 2)
    neighbor3 = MatchNeighbor('7sLQGgXFs4LaGAaDErPwOl', 5)

    response.extend([[neighbor1, neighbor2, neighbor3]])

    return response


class MatchServiceClient(Client):
  """ gRPC match service implementation. """

  def __init__(self, config_facade: ConfigFacade) -> None:
    self._region = env.env_util.get_environment_variable('REGION',
                                                         default=REGION_DEFAULT)
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
        num_neighbors=num_recos)

    return match_neighbors

  def get_service_metadata(self) -> None:
    index_endpoint_filter = f'labels.environment={self._environment}'
    index_endpoint_filter += f' AND labels.region={self._region}'
    index_endpoint = aiplatform.MatchingEngineIndexEndpoint.list(
        filter=index_endpoint_filter,
        project=self._project_id,
        location=self._region)[0]
    self._deployed_index_id = index_endpoint.deployed_indexes[0].id

    self._index_endpoint = index_endpoint
