from abc import abstractmethod
from http import HTTPStatus
from abc import ABC

class ResponseBuilder(ABC):
    def set_spotify_tracks_response(self, spotify_tracks_response) -> None:
        self._spotify_tracks_response = spotify_tracks_response

    def set_vertex_ann_response(self, vertex_ann_response) -> None:
        self._vertex_ann_response = vertex_ann_response
    
    def set_request(self, request) -> None:
        self._request = request

    @abstractmethod
    def build_response(self) -> dict:
        pass

class BadRequestResponseBuilder(ResponseBuilder):
    def __init__(self) -> None:
        self._response_code = HTTPStatus.BAD_REQUEST.value

    def build_response(self) -> dict:
        response = {
            "message": "Bad request.",
            "status": self._response_code
        }
        return response

class NotFoundResponseBuilder(ResponseBuilder):
    def __init__(self) -> None:
        self._response_code = HTTPStatus.NOT_FOUND.value
    
    def build_response(self) -> dict:
        response = {
            "message": "Invalid track id.",
            "status": self._response_code
        }
        return response

class OkResponseBuilder(ResponseBuilder):
    def __init__(self) -> None:
        self._response_code = HTTPStatus.OK.value
    
    def build_response(self) -> dict:
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
