from abc import abstractmethod
from http import HTTPStatus
from abc import ABC

class ResponseBuilder(ABC):
    @abstractmethod
    def build_response(self, recos_dict: dict, id: str, size: int) -> dict:
        pass

class BadRequestResponseBuilder(ResponseBuilder):
    def __init__(self) -> None:
        self._response_code = HTTPStatus.BAD_REQUEST.value

    def build_response(self, recos_dict: dict, id: str, size: int) -> dict:
        response = {
            "message": "Bad request.",
            "status": self._response_code
        }
        return response

class NotFoundResponseBuilder(ResponseBuilder):
    def __init__(self) -> None:
        self._response_code = HTTPStatus.NOT_FOUND.value
    
    def build_response(self, recos_dict: dict, id: str, size: int) -> dict:
        response = {
            "message": "Invalid track id: {}".format(id),
            "status": self._response_code
        }
        return response

class OkResponseBuilder(ResponseBuilder):
    def __init__(self) -> None:
        self._response_code = HTTPStatus.OK.value
    
    def build_response(self, recos_dict: dict, id: str, size: int) -> dict:
        return {} # TODO

class ResponseBuilderFactory():
    def __init__(self, bad_request_builder, not_found_builder, ok_builder) -> None:
        self._bad_request_builder = bad_request_builder
        self._not_found_builder = not_found_builder
        self._ok_builder = ok_builder
    
    def get_builder(self, status_code) -> ResponseBuilder:
        builder = None
        if status_code == HTTPStatus.BAD_REQUEST.value:
            builder = self._bad_request_builder
        elif status_code == HTTPStatus.NOT_FOUND.value:
            builder = self._not_found_builder
        elif status_code == HTTPStatus.OK.value:
            builder = self._ok_builder
        else:
            raise ValueError('Invalid or unsupported status code: {}'.format(status_code))
        return builder
