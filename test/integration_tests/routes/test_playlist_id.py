""" Integration test module for playlist resources. """
import unittest
from src.api.app import flask_app
from werkzeug.test import TestResponse


class PlaylistResourceTestSuite(unittest.TestCase):
  """ Integration test suite for POST::v1/{user_id}/{track_id} API. """

  def setUp(self) -> None:
    self._client = flask_app.test_client()
    self._user_id = 'nteshima'
    self._track_id = '6AUlMVr80H8KGVTGeJlpbp'
    self._uri = f'/v1/playlist/{self._user_id}/{self._track_id}'

  def test_should_return_400_for_invalid_size(self) -> None:
    pass

  def test_should_return_401_for_invalid_authorization_header(self) -> None:
    pass

  def test_should_return_403_for_insufficient_authorization_scope(self) -> None:
    pass
