""" Integration test module for playlist resources. """
import unittest
from src.api.app import flask_app
from src.api.clients.spotify_auth_client import spotify_auth_client


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
    headers = {'Authorization': 'Invalid token'}

    response = self._spotifind_client.post(self._uri, headers=headers)

    self.assertEqual(401, response.status_code)

  def test_should_return_403_for_insufficient_authorization_scope(self) -> None:
    token_bearer = self._spotify_auth_client.get_bearer_token()
    headers = {'Authorization': f'Bearer {token_bearer}'}

    response = self._spotifind_client.post(self._uri, headers=headers)

    self.assertEqual(403, response.status_code)
