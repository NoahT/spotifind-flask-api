""" Module for response building for all APIs. """
from abc import ABC, abstractmethod
from http import HTTPStatus

from werkzeug.datastructures import Headers


class Response():
  """ Model class containing response metadata. """

  def __init__(self, response: dict, response_code: int,
               response_headers: list) -> None:
    self.response = response
    self.response_code = response_code
    self.response_headers = Headers()
    self.add_response_headers(response_headers=response_headers)

  def add_response_headers(self, response_headers) -> None:
    for header in (response_headers or []):
      self.response_headers.add(_key=header[0], _value=header[1])


class ResponseBuilder(ABC):
  """ Abstract base class for response building on all APIs. """

  @abstractmethod
  def build_response(self, recos_response: list, track_id: str, size: int,
                     **kwargs: dict) -> Response:
    pass


class BadRequestResponseBuilder(ResponseBuilder):
  """ Response builder for 400 (Bad Request) status code. """

  def __init__(self) -> None:
    self._response_code = HTTPStatus.BAD_REQUEST.value

  def build_response(self, recos_response: list, track_id: str, size: int,
                     **kwargs: dict) -> Response:
    response = {'message': 'Bad request.', 'status': self._response_code}
    return Response(response, self._response_code, [])


class UnauthorizedResponseBuilder(ResponseBuilder):
  """ Response builder for 401 (Unauthorized) status code. """

  def __init__(self) -> None:
    self._response_code = HTTPStatus.UNAUTHORIZED.value

  def build_response(self, recos_response: list, track_id: str, size: int,
                     **kwargs: dict) -> Response:
    response = {
        'message': 'Valid authentication credentials not provided.',
        'status': self._response_code
    }

    return Response(response, self._response_code, [])


class ForbiddenResponseBuilder(ResponseBuilder):
  """ Response builder for 403 (Forbidden) status code. """

  def __init__(self) -> None:
    self._response_code = HTTPStatus.FORBIDDEN.value

  def build_response(self, recos_response: list, track_id: str, size: int,
                     **kwargs: dict) -> Response:
    response = {
        'message': 'Insufficient authentication credentials.',
        'status': self._response_code
    }

    return Response(response, self._response_code, [])


class NotFoundResponseBuilder(ResponseBuilder):
  """ Response builder for 404 (Not Found) status code. """

  def __init__(self) -> None:
    self._response_code = HTTPStatus.NOT_FOUND.value

  def build_response(self, recos_response: list, track_id: str, size: int,
                     **kwargs: dict) -> Response:
    response = {
        'message': f'Invalid track id: {track_id}',
        'status': self._response_code
    }
    return Response(response, self._response_code, [])


class InternalServerErrorResponseBuilder(ResponseBuilder):
  """ Response builder for 500 (Internal Server Error) status code. """

  def __init__(self) -> None:
    self._response_code = HTTPStatus.INTERNAL_SERVER_ERROR.value

  def build_response(self, recos_response: list, track_id: str, size: int,
                     **kwargs: dict) -> Response:
    response = {
        'message':
            'An unexpected error occurred. Please contact a contributor ' +
            'for assistance.',
        'status':
            self._response_code
    }
    return Response(response, self._response_code, [])


class CreatedResponseBuilder(ResponseBuilder):
  """ Response builder for 201 (Created) status code. """

  def __init__(self) -> None:
    self._response_code = HTTPStatus.CREATED.value

  def build_response(self, recos_response: list, track_id: str, size: int,
                     **kwargs: dict) -> Response:
    playlist_id = kwargs['playlist_id']
    playlist_uri_abs = f'https://api.spotify.com/v1/playlists/{playlist_id}'
    location_response_header = ('Location', playlist_uri_abs)

    return Response({}, self._response_code, [location_response_header])


class OkResponseBuilder(ResponseBuilder):
  """ Response builder for 200 (OK) status code. """

  def __init__(self) -> None:
    self._response_code = HTTPStatus.OK.value

  def build_response(self, recos_response: list, track_id: str, size: int,
                     **kwargs: dict) -> Response:
    print(recos_response)
    response = {'request': {'track': {'id': track_id}, 'size': size}}
    recos = []
    neighbors = [{'id': match_neighbor.id} for match_neighbor in recos_response]
    for reco in neighbors:
      if track_id != reco['id']:
        recos.append({'id': reco['id']})

    response['recos'] = recos[:size]

    return Response(response, self._response_code, [])


class ResponseBuilderFactory():
  """ Factory pattern class. Get response builder based on status code. """

  def __init__(self, **kwargs) -> None:
    self._bad_request_builder = kwargs['bad_request_builder']
    self._unauthorized_builder = kwargs['unauthorized_builder']
    self._forbidden_builder = kwargs['forbidden_builder']
    self._not_found_builder = kwargs['not_found_builder']
    self._internal_server_error_builder = kwargs[
        'internal_server_error_builder']
    self._ok_builder = kwargs['ok_builder']
    self._created_builder = kwargs['created_builder']

  def get_builder(self, status_code: int) -> ResponseBuilder:
    builder = None
    if status_code == HTTPStatus.BAD_REQUEST.value:
      builder = self._bad_request_builder
    elif status_code == HTTPStatus.UNAUTHORIZED.value:
      builder = self._unauthorized_builder
    elif status_code == HTTPStatus.FORBIDDEN.value:
      builder = self._forbidden_builder
    elif status_code == HTTPStatus.NOT_FOUND.value:
      builder = self._not_found_builder
    elif status_code == HTTPStatus.INTERNAL_SERVER_ERROR.value:
      builder = self._internal_server_error_builder
    elif status_code == HTTPStatus.OK.value:
      builder = self._ok_builder
    elif status_code == HTTPStatus.CREATED.value:
      builder = self._created_builder
    else:
      raise ValueError(f'Invalid or unsupported status code: {status_code}')
    return builder
