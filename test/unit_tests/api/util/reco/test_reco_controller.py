""" reco_controller unit test module. """
import unittest
from unittest.mock import patch, Mock
from http import HTTPStatus
from requests import HTTPError as ClientHTTPError
from src.api.schemas.response import Response, BadRequestResponseBuilder, UnauthorizedResponseBuilder, ForbiddenResponseBuilder, NotFoundResponseBuilder
from src.api.util.reco import reco_controller


def get_create_playlist_side_effect(status_code):

  # pylint: disable-next=unused-argument
  def side_effect(user_id, track_id, user_token, size):
    mock_response = Mock()
    mock_response.status_code = status_code
    raise ClientHTTPError(response=mock_response)

  return side_effect


def get_recos_side_effect(status_code):

  # pylint: disable-next=unused-argument
  def side_effect(track_id, size):
    mock_response = Mock()
    mock_response.status_code = status_code
    raise ClientHTTPError(response=mock_response)

  return side_effect


class V1RecoControllerTestSuite(unittest.TestCase):
  """ Unit test suite for V1RecoController. """

  @patch('src.api.schemas.response.ResponseBuilderFactory')
  @patch('src.api.util.reco.reco_adapter.V1RecoAdapter')
  def setUp(self, reco_adapter, response_builder_factory) -> None:
    bad_request_response_builder = Mock(BadRequestResponseBuilder)
    bad_request_response_builder.build_response.return_value = Response(
        None, 400, response_headers=[])
    unauthorized_response_builder = Mock(UnauthorizedResponseBuilder)
    unauthorized_response_builder.build_response.return_value = Response(
        None, 401, response_headers=[])
    forbidden_response_builder = Mock(ForbiddenResponseBuilder)
    forbidden_response_builder.build_response.return_value = Response(
        None, 403, response_headers=[])
    not_found_response_builder = Mock(NotFoundResponseBuilder)
    not_found_response_builder.build_response.return_value = Response(
        None, 404, response_headers=[])
    self.bad_request_response_builder = bad_request_response_builder
    self.not_found_response_builder = not_found_response_builder

    def factory_side_effect(**kwargs):
      response_builder = None
      status_code = kwargs['status_code']
      if status_code == HTTPStatus.NOT_FOUND.value:
        response_builder = not_found_response_builder
      elif status_code == HTTPStatus.UNAUTHORIZED.value:
        response_builder = unauthorized_response_builder
      elif status_code == HTTPStatus.FORBIDDEN.value:
        response_builder = forbidden_response_builder
      else:
        response_builder = bad_request_response_builder

      return response_builder

    response_builder_factory.get_builder.side_effect = factory_side_effect
    self.v1_reco_controller = reco_controller.V1RecoController(
        reco_adapter, response_builder_factory)

  def test_should_return_400_response_on_invalid_client_request(self) -> None:
    side_effect_400 = get_recos_side_effect(400)
    get_recos = self.v1_reco_controller.reco_adapter.get_recos
    get_recos.side_effect = side_effect_400
    reco_response = self.v1_reco_controller.get_recos('invalid', '5')
    self.assertEqual(400, reco_response.response_code)

  def test_should_return_200_response_on_valid_client_request(self) -> None:
    mock_response = Response(
        {
            'request': {
                'track': {
                    'id': 'track_id'
                },
                'size': 5
            },
            'recos': [
                {
                    'id': 'reco1'
                },
                {
                    'id': 'reco2'
                },
                {
                    'id': 'reco3'
                },
            ]
        },
        200,
        response_headers=[])
    self.v1_reco_controller.reco_adapter.get_recos.return_value = mock_response

    reco_response = self.v1_reco_controller.get_recos('track_id', '5')

    self.assertEqual(mock_response.response_code, reco_response.response_code)
    self.assertEqual(mock_response.response, reco_response.response)

  def test_should_return_400_on_v1_playlist_for_invalid_client_request(
      self) -> None:
    create_playlist = self.v1_reco_controller.reco_adapter.create_playlist
    side_effect_400 = get_create_playlist_side_effect(400)
    create_playlist.side_effect = side_effect_400
    create_playlist_response = self.v1_reco_controller.create_playlist(
        user_id='user_id',
        track_id='track_id',
        user_token='user_token',
        size='5')
    self.assertEqual(400, create_playlist_response.response_code)

  def test_should_return_401_on_v1_playlist_for_missing_authorization(
      self) -> None:
    create_playlist = self.v1_reco_controller.reco_adapter.create_playlist
    side_effect_401 = get_create_playlist_side_effect(401)
    create_playlist.side_effect = side_effect_401
    create_playlist_response = self.v1_reco_controller.create_playlist(
        user_id='user_id',
        track_id='track_id',
        user_token='user_token',
        size='5')
    self.assertEqual(401, create_playlist_response.response_code)

  def test_should_return_403_on_v1_playlist_for_insufficient_authorization(
      self) -> None:
    create_playlist = self.v1_reco_controller.reco_adapter.create_playlist
    side_effect_403 = get_create_playlist_side_effect(403)
    create_playlist.side_effect = side_effect_403
    create_playlist_response = self.v1_reco_controller.create_playlist(
        user_id='user_id',
        track_id='track_id',
        user_token='user_token',
        size='5')
    self.assertEqual(403, create_playlist_response.response_code)
