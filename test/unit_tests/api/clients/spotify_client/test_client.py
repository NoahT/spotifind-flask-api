""" Unit test module for spotify_client. """
from unittest.mock import Mock
import unittest
from src.api.clients.spotify_client.client import SpotifyClient
import requests


class SpotifyClientTestSuite(unittest.TestCase):
  """ Unit test suite for SpotifyClient. """

  def setUp(self) -> None:
    logging_client = Mock()
    auth_client = Mock()
    config_facade = Mock()
    config_facade.get_spotify_client_config.return_value = {
        'CONNECT_TIMEOUT': 0.500,
        'READ_TIMEOUT': 0.500
    }
    self._spotify_client = SpotifyClient(auth_client, logging_client,
                                         config_facade)
    self._response = requests.Response()

  def test_should_raise_error_for_4xx_response_on_v1_tracks(self):
    self._response.status_code = 400
    requests.get = Mock(return_value=self._response)
    self._spotify_client.get_bearer_token = Mock(return_value='Bearer token')

    self.assertRaises(requests.HTTPError, self._spotify_client.v1_tracks, 'id')

  def test_should_raise_error_for_5xx_response_on_v1_tracks(self):
    self._response.status_code = 500
    requests.get = Mock(return_value=self._response)
    self._spotify_client.get_bearer_token = Mock(return_value='Bearer token')

    self.assertRaises(requests.HTTPError, self._spotify_client.v1_tracks, 'id')

  def test_should_return_json_for_2xx_response_on_v1_tracks(self):
    self._response.status_code = 200
    requests.get = Mock(return_value=self._response)
    requests.Response.json = Mock(return_value={})
    self._spotify_client.get_bearer_token = Mock(return_value='Bearer token')

    response = self._spotify_client.v1_tracks('id')

    self.assertEqual({}, response)

  def test_should_raise_error_for_4xx_response_on_v1_tracks_bulk(self):
    self._response.status_code = 400
    requests.get = Mock(return_value=self._response)
    self._spotify_client.get_bearer_token = Mock(return_value='Bearer token')

    self.assertRaises(requests.HTTPError, self._spotify_client.v1_tracks_bulk,
                      ['id_1', 'id_2'])

  def test_should_raise_error_for_5xx_response_on_v1_tracks_bulk(self):
    self._response.status_code = 500
    requests.get = Mock(return_value=self._response)
    self._spotify_client.get_bearer_token = Mock(return_value='Bearer token')

    self.assertRaises(requests.HTTPError, self._spotify_client.v1_tracks_bulk,
                      ['id_1', 'id_2'])

  def test_should_return_json_for_2xx_response_on_v1_tracks_bulk(self):
    self._response.status_code = 200
    requests.get = Mock(return_value=self._response)
    requests.Response.json = Mock(return_value={})
    self._spotify_client.get_bearer_token = Mock(return_value='Bearer token')

    response = self._spotify_client.v1_tracks_bulk(['id_1', 'id_2'])

    self.assertEqual({}, response)

  def test_should_raise_error_for_4xx_response_on_v1_audio_features(self):
    self._response.status_code = 400
    requests.get = Mock(return_value=self._response)
    self._spotify_client.get_bearer_token = Mock(return_value='Bearer token')

    self.assertRaises(requests.HTTPError,
                      self._spotify_client.v1_audio_features, 'id')

  def test_should_raise_error_for_5xx_response_on_v1_audio_features(self):
    self._response.status_code = 500
    requests.get = Mock(return_value=self._response)
    self._spotify_client.get_bearer_token = Mock(return_value='Bearer token')

    self.assertRaises(requests.HTTPError,
                      self._spotify_client.v1_audio_features, 'id')

  def test_should_return_json_for_2xx_response_on_v1_audio_features(self):
    self._response.status_code = 200
    requests.get = Mock(return_value=self._response)
    requests.Response.json = Mock(return_value={})
    self._spotify_client.get_bearer_token = Mock(return_value='Bearer token')

    response = self._spotify_client.v1_audio_features('id')

    self.assertEqual({}, response)

  def test_should_return_json_for_2xx_response_on_v1_create_playlist(self):
    self._response.status_code = 200
    requests.post = Mock(return_value=self._response)
    requests.Response.json = Mock(return_value={})

    response = self._spotify_client.v1_create_playlist('user_id', 'user_token')

    self.assertEqual({}, response)

  def test_should_raise_error_for_4xx_response_on_v1_create_playlist(self):
    self._response.status_code = 400
    requests.post = Mock(return_value=self._response)

    self.assertRaises(requests.HTTPError,
                      self._spotify_client.v1_create_playlist, 'user_id',
                      'user_token')

  def test_should_raise_error_for_5xx_response_on_v1_create_playlist(self):
    self._response.status_code = 500
    requests.post = Mock(return_value=self._response)

    self.assertRaises(requests.HTTPError,
                      self._spotify_client.v1_create_playlist, 'user_id',
                      'user_token')

  def test_should_return_json_for_2xx_response_on_v1_playlist_tracks(self):
    self._response.status_code = 200
    requests.post = Mock(return_value=self._response)
    requests.Response.json = Mock(return_value={})
    payload = {
        'uris': [
            'spotify:track:7Bwaf8up63T37RzgWt7uaL',
            'spotify:track:35RnMOsCCAySWKGdl2IcjC'
        ]
    }

    response = self._spotify_client.v1_playlist_tracks('playlist_id', payload,
                                                       'user_token')

    self.assertEqual({}, response)

  def test_should_raise_error_for_4xx_response_on_v1_playlist_tracks(self):
    self._response.status_code = 400
    requests.post = Mock(return_value=self._response)
    payload = {
        'uris': [
            'spotify:track:7Bwaf8up63T37RzgWt7uaL',
            'spotify:track:35RnMOsCCAySWKGdl2IcjC'
        ]
    }

    self.assertRaises(requests.HTTPError,
                      self._spotify_client.v1_playlist_tracks, 'playlist_id',
                      payload, 'user_token')

  def test_should_raise_error_for_5xx_response_on_v1_playlist_tracks(self):
    self._response.status_code = 500
    requests.post = Mock(return_value=self._response)
    payload = {
        'uris': [
            'spotify:track:7Bwaf8up63T37RzgWt7uaL',
            'spotify:track:35RnMOsCCAySWKGdl2IcjC'
        ]
    }

    self.assertRaises(requests.HTTPError,
                      self._spotify_client.v1_playlist_tracks, 'playlist_id',
                      payload, 'user_token')

  def test_should_return_correct_authorization_header(self):
    auth_client = Mock()
    auth_client.get_bearer_token.return_value = {'access_token': 'token'}
    logging_client = Mock()
    config_facade = Mock()
    config_facade.get_spotify_client_config.return_value = {
        'CONNECT_TIMEOUT': 0.500,
        'READ_TIMEOUT': 0.500
    }
    self._spotify_client = SpotifyClient(auth_client, logging_client,
                                         config_facade)

    bearer_token = self._spotify_client.get_bearer_token()

    self.assertEqual('Bearer token', bearer_token)