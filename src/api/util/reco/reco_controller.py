from abc import ABC, abstractmethod
from urllib.error import HTTPError
from requests import HTTPError as ClientHTTPError
import src.api.schemas.response as response
from . import reco_adapter

class RecoController(ABC):
    @abstractmethod
    def get_recos(self, id: str, size: int) -> response.Response:
        pass

class V1RecoController(RecoController):
    def __init__(self, reco_adapter: reco_adapter.RecoAdapter, response_builder_factory: response.ResponseBuilderFactory) -> None:
        self._reco_adapter = reco_adapter
        self._response_builder_factory = response_builder_factory

    def get_recos(self, id: str, size: int) -> response.Response:
        recos_response = None
        try:
            recos_response = self._reco_adapter.get_recos(id, size)
        except HTTPError as http_error:
            print(http_error.__str__())
            recos_response = self._response_builder_factory.get_builder(status_code=http_error.code).build_response(recos_response=None, id=id, size=size)
        except ClientHTTPError as client_http_error:
            print(client_http_error.__str__())
            recos_response = self._response_builder_factory.get_builder(status_code=client_http_error.response.status_code).build_response(recos_response=None, id=id, size=size)
        
        return recos_response

