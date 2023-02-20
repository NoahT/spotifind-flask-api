""" Integration test module for playlist resources. """
import unittest
from src.api.app import flask_app
from src.api.clients.spotify_auth_client import spotify_auth_client
from werkzeug.datastructures import Headers


class PlaylistResourceTestSuite(unittest.TestCase):
  """ Integration test suite for POST::v1/{user_id}/{track_id} API. """

  def setUp(self) -> None:
    self._spotifind_client = flask_app.test_client()
    self._spotify_auth_client = spotify_auth_client
    self._user_id = 'noahteshima'
    self._track_id = '6AUlMVr80H8KGVTGeJlpbp'
    self._uri = f'/v1/playlist/{self._user_id}/{self._track_id}'

  def test_should_return_400_for_invalid_size(self) -> None:
    response = self._spotifind_client.post(f'{self._uri}?size=0')

    self.assertEqual(400, response.status_code)

  def test_should_return_401_for_invalid_authorization_header(self) -> None:
    response_401 = {
        'message': 'Valid authentication credentials not provided.',
        'status': 401
    }
    headers = Headers()
    headers.add('Authorization', 'Invalid token')

    response = self._spotifind_client.post(self._uri, headers=headers)
    response_json = response.json

    self.assertIsNotNone(response_json)
    self.assertEqual(response_401, response_json)

  def test_should_return_403_for_insufficient_authorization_scope(self) -> None:
    response_403 = {
        'message': 'Insufficient authentication credentials.',
        'status': 403
    }
    token_bearer = self._spotify_auth_client.get_bearer_token()
    token_bearer = token_bearer['access_token']
    headers = Headers()
    headers.add('Authorization', f'Bearer {token_bearer}')

    response = self._spotifind_client.post(self._uri, headers=headers)
    response_json = response.json

    self.assertIsNotNone(response_json)
    self.assertEqual(response_403, response_json)
