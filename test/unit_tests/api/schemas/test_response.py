""" Unit test module for  """
import unittest
from src.api.schemas.response import (
    BadRequestResponseBuilder, UnauthorizedResponseBuilder,
    ForbiddenResponseBuilder, NotFoundResponseBuilder,
    InternalServerErrorResponseBuilder, OkResponseBuilder,
    CreatedResponseBuilder, ResponseBuilderFactory)
from http import HTTPStatus
from google.cloud.aiplatform.matching_engine.matching_engine_index_endpoint import MatchNeighbor


class ResponseFactoryTestSuite(unittest.TestCase):
  """ Unit test suite for ResponseFactory. """

  def setUp(self) -> None:
    self._bad_request_response_builder = BadRequestResponseBuilder()
    self._unauthorized_response_builder = UnauthorizedResponseBuilder()
    self._forbidden_response_builder = ForbiddenResponseBuilder()
    self._not_found_response_builder = NotFoundResponseBuilder()
    self._internal_server_error_builder = InternalServerErrorResponseBuilder()
    self._ok_response_builder = OkResponseBuilder()
    self._created_response_builder = CreatedResponseBuilder()
    self._response_builder_factory = ResponseBuilderFactory(
        bad_request_builder=self._bad_request_response_builder,
        unauthorized_builder=self._unauthorized_response_builder,
        forbidden_builder=self._forbidden_response_builder,
        not_found_builder=self._not_found_response_builder,
        internal_server_error_builder=self._internal_server_error_builder,
        ok_builder=self._ok_response_builder,
        created_builder=self._created_response_builder)

  def test_should_return_bad_request_response_builder_on_400(self):
    response_builder = self._response_builder_factory.get_builder(
        HTTPStatus.BAD_REQUEST.value)

    self.assertIs(response_builder, self._bad_request_response_builder)

  def test_should_return_not_found_response_builder_on_404(self):
    response_builder = self._response_builder_factory.get_builder(
        HTTPStatus.NOT_FOUND.value)

    self.assertIs(response_builder, self._not_found_response_builder)

  def test_should_return_not_found_response_builder_on_500(self):
    response_builder = self._response_builder_factory.get_builder(
        HTTPStatus.INTERNAL_SERVER_ERROR.value)

    self.assertIs(response_builder, self._internal_server_error_builder)

  def test_should_return_ok_response_builder_on_200(self):
    response_builder = self._response_builder_factory.get_builder(
        HTTPStatus.OK.value)

    self.assertIs(response_builder, self._ok_response_builder)

  def test_should_raise_error_when_unsupported_status_used(self):
    self.assertRaises(ValueError, self._response_builder_factory.get_builder,
                      HTTPStatus.BAD_GATEWAY.value)


class ResponseBuilderTestSuite(unittest.TestCase):
  """ Unit test suite for ResponseBuilder. """

  def test_should_properly_build_400_response(self):
    bad_request_response = BadRequestResponseBuilder().build_response(
        recos_response={}, track_id='123', size=5)
    response_400 = {'message': 'Bad request.', 'status': 400}

    self.assertEqual(response_400, bad_request_response.response)
    self.assertEqual(400, bad_request_response.response_code)

  def test_should_properly_build_401_response(self):
    unauthorized_response = UnauthorizedResponseBuilder().build_response(
        recos_response={}, track_id='123', size=5)
    response_401 = {
        'message': 'Valid authentication credentials not provided.',
        'status': 401
    }

    self.assertEqual(response_401, unauthorized_response.response)
    self.assertEqual(401, unauthorized_response.response_code)

  def test_should_properly_build_403_response(self):
    forbidden_response = ForbiddenResponseBuilder().build_response(
        recos_response={}, track_id='123', size=5)
    response_403 = {
        'message': 'Insufficient authentication credentials.',
        'status': 403
    }

    self.assertEqual(response_403, forbidden_response.response)
    self.assertEqual(403, forbidden_response.response_code)

  def test_should_properly_build_404_response(self):
    not_found_response = NotFoundResponseBuilder().build_response(
        recos_response={}, track_id='123', size=5)
    response_404 = {'message': 'Invalid track id: 123', 'status': 404}

    self.assertEqual(response_404, not_found_response.response)
    self.assertEqual(404, not_found_response.response_code)

  def test_should_properly_build_500_response(self):
    internal_server_error_response = InternalServerErrorResponseBuilder(
    ).build_response(recos_response={}, track_id='123', size=5)
    response_500 = {
        'message':
            'An unexpected error occurred. ' +
            'Please contact a contributor for assistance.',
        'status':
            500
    }

    self.assertEqual(response_500, internal_server_error_response.response)
    self.assertEqual(500, internal_server_error_response.response_code)

  def test_should_properly_build_200_response(self):
    recos = [
        MatchNeighbor('7C48cUjCGx14K5b41e9vTD', 1.0),
        MatchNeighbor('3x7gMvCsL1SS6THGwB55Pm', 2.0),
        MatchNeighbor('7sLQGgXFs4LaGAaDErPwOl', 5.0)
    ]
    expected_response = {
        'recos': [{
            'id': '7C48cUjCGx14K5b41e9vTD'
        }, {
            'id': '3x7gMvCsL1SS6THGwB55Pm'
        }],
        'request': {
            'size': 2,
            'track': {
                'id': '123'
            }
        }
    }
    ok_response = OkResponseBuilder().build_response(recos_response=recos,
                                                     track_id='123',
                                                     size=2)

    self.assertEqual(expected_response, ok_response.response)
    self.assertEqual(200, ok_response.response_code)

  def test_should_properly_build_200_response_with_input_as_neighbor(self):
    recos = [
        MatchNeighbor('123', 0.0),
        MatchNeighbor('3x7gMvCsL1SS6THGwB55Pm', 2.0),
        MatchNeighbor('7sLQGgXFs4LaGAaDErPwOl', 5.0)
    ]
    expected_response = {
        'recos': [{
            'id': '3x7gMvCsL1SS6THGwB55Pm'
        }, {
            'id': '7sLQGgXFs4LaGAaDErPwOl'
        }],
        'request': {
            'size': 2,
            'track': {
                'id': '123'
            }
        }
    }
    ok_response = OkResponseBuilder().build_response(recos_response=recos,
                                                     track_id='123',
                                                     size=2)

    self.assertEqual(expected_response, ok_response.response)
    self.assertEqual(200, ok_response.response_code)

  def test_should_properly_build_201_response(self):
    created_response = CreatedResponseBuilder().build_response(
        recos_response={}, track_id='123', size=5, playlist_id='playlist_id')

    self.assertEqual({}, created_response.response)
    self.assertEqual(201, created_response.response_code)
    self.assertEqual(
        'https://api.spotify.com/v1/playlists/playlist_id',
        created_response.response_headers.get('Location', type=str))
