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

  def test_should_create_sublists_from_track_id_list_with_multiple_sublists(
      self) -> None:
    track_ids = [
        '7Fu7avD3IaqVDprclBEyrM', '78cIbVjU1xn7mbQ9i35avl',
        '6tSa0K6KMXscRwRQle0HVX', '6dNvZbCd4XOr4pqU76TB3u',
        '2xXpu16xh9EZAi9o4lCeK6'
    ]

    track_id_sublists = self._spotify_client.get_track_id_sublists(
        track_ids=track_ids, sublist_size=2)

    self.assertIsNotNone(track_id_sublists)
    self.assertEqual(3, len(track_id_sublists))

    track_id_sublist1 = track_id_sublists[0]
    self.assertIsNotNone(track_id_sublist1)
    self.assertEqual(['7Fu7avD3IaqVDprclBEyrM', '78cIbVjU1xn7mbQ9i35avl'],
                     track_id_sublist1)

    track_id_sublist2 = track_id_sublists[1]
    self.assertIsNotNone(track_id_sublist2)
    self.assertEqual(['6tSa0K6KMXscRwRQle0HVX', '6dNvZbCd4XOr4pqU76TB3u'],
                     track_id_sublist2)

    track_id_sublist3 = track_id_sublists[2]
    self.assertIsNotNone(track_id_sublist3)
    self.assertEqual(['2xXpu16xh9EZAi9o4lCeK6'], track_id_sublist3)

  def test_should_create_sublist_from_track_id_list_with_singular_sublist(
      self) -> None:
    track_ids = [
        '7Fu7avD3IaqVDprclBEyrM', '78cIbVjU1xn7mbQ9i35avl',
        '6tSa0K6KMXscRwRQle0HVX', '6dNvZbCd4XOr4pqU76TB3u',
        '2xXpu16xh9EZAi9o4lCeK6'
    ]

    track_id_sublists = self._spotify_client.get_track_id_sublists(
        track_ids=track_ids, sublist_size=50)

    self.assertIsNotNone(track_id_sublists)
    self.assertEqual(1, len(track_id_sublists))

    track_id_sublist1 = track_id_sublists[0]
    self.assertIsNotNone(track_id_sublist1)
    self.assertEqual(track_ids, track_id_sublist1)
