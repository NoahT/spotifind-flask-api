from abc import abstractmethod
from http import HTTPStatus
from abc import ABC

class Response():
    def __init__(self, response: dict, response_code: int) -> None:
        self.response = response
        self.response_code = response_code

class ResponseBuilder(ABC):
    @abstractmethod
    def build_response(self, recos_response: list, id: str, size: int) -> Response:
        pass

class BadRequestResponseBuilder(ResponseBuilder):
    def __init__(self) -> None:
        self._response_code = HTTPStatus.BAD_REQUEST.value

    def build_response(self, recos_response: list, id: str, size: int) -> Response:
        response = {
            'message': 'Bad request.',
            'status': self._response_code
        }
        return Response(response=response, response_code=self._response_code)

class NotFoundResponseBuilder(ResponseBuilder):
    def __init__(self) -> None:
        self._response_code = HTTPStatus.NOT_FOUND.value
    
    def build_response(self, recos_response: list, id: str, size: int) -> Response:
        response = {
            'message': 'Invalid track id: {}'.format(id),
            'status': self._response_code
        }
        return Response(response=response, response_code=self._response_code)

class InternalServerErrorResponseBuilder(ResponseBuilder):
    def __init__(self) -> None:
        self._response_code = HTTPStatus.INTERNAL_SERVER_ERROR.value
    
    def build_response(self, recos_response: list, id: str, size: int) -> Response:
        response = {
            'message': 'An unexpected error occurred. Please contact a contributor for assistance.',
            'status': self._response_code
        }
        return Response(response=response, response_code=self._response_code)

class OkResponseBuilder(ResponseBuilder):
    def __init__(self) -> None:
        self._response_code = HTTPStatus.OK.value
    
    def build_response(self, recos_response: list, id: str, size: int) -> Response:
        print(recos_response)
        response = {
            'request': {
                'track': {
                    'id': id
                },
                'size': size
            }
        }
        recos = []
        neighbors = [{ 'id': match_neighbor.id } for match_neighbor in recos_response]
        for reco in neighbors:
            if id != reco['id']:
                recos.append({ 'id': reco['id'] })
        
        response['recos'] = recos[:size]

        return Response(response=response, response_code=self._response_code)

class ResponseBuilderFactory():
    def __init__(self, bad_request_builder=BadRequestResponseBuilder(), not_found_builder=NotFoundResponseBuilder(), internal_server_error_builder=InternalServerErrorResponseBuilder(), ok_builder=OkResponseBuilder()) -> None:
        self._bad_request_builder = bad_request_builder
        self._not_found_builder = not_found_builder
        self._internal_server_error_builder = internal_server_error_builder
        self._ok_builder = ok_builder
    
    def get_builder(self, status_code: int) -> ResponseBuilder:
        builder = None
        if status_code == HTTPStatus.BAD_REQUEST.value:
            builder = self._bad_request_builder
        elif status_code == HTTPStatus.NOT_FOUND.value:
            builder = self._not_found_builder
        elif status_code == HTTPStatus.INTERNAL_SERVER_ERROR.value:
            builder = self._internal_server_error_builder
        elif status_code == HTTPStatus.OK.value:
            builder = self._ok_builder
        else:
            raise ValueError('Invalid or unsupported status code: {}'.format(status_code))
        return builder
