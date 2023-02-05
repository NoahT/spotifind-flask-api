""" reco_adapter unit test module. """
from http import HTTPStatus
from google.cloud.aiplatform.matching_engine.matching_engine_index_endpoint import MatchNeighbor
from urllib.error import HTTPError
from unittest.mock import patch, Mock
from src.api.util.reco import reco_adapter
from src.api.schemas import response
import unittest


class V1RecoAdapterTestSuite(unittest.TestCase):
  """ Unit test suite for V1RecoAdapter """

  @patch('src.api.schemas.response.ResponseBuilderFactory')
  @patch('src.api.clients.matching_engine_client.client_aggregator' +
         '.ClientAggregator')
  @patch('src.api.clients.spotify_client.client.Client')
  def setUp(self, spotify_client, client_aggregator,
            response_builder_factory) -> None:
    ok_response_builder = Mock(response.OkResponseBuilder)
    ok_response_builder.build_response.return_value = response.Response(
        response={
            'recos': [{
                'id': '63h44N1oLElnzut7RxZt6Z'
            }, {
                'id': '35RnMOsCCAySWKGdl2IcjC'
            }]
        },
        response_code=200,
        response_headers=[])
    self.ok_response_builder = ok_response_builder
    created_response_builder = Mock(response.CreatedResponseBuilder)
    created_response_builder.build_response.return_value = response.Response(
        response={}, response_code=201, response_headers=[])
    self.created_response_builder = created_response_builder

    def factory_side_effect(**kwargs):
      response_builder = None
      status_code = kwargs['status_code']
      if status_code == HTTPStatus.OK.value:
        response_builder = ok_response_builder
      elif status_code == HTTPStatus.CREATED.value:
        response_builder = created_response_builder

      return response_builder

    response_builder_factory.get_builder.side_effect = factory_side_effect

    self.reco_adapter = reco_adapter.V1RecoAdapter(
        spotify_client=spotify_client,
        client_aggregator=client_aggregator,
        response_builder_factory=response_builder_factory)

  def test_should_return_recos_on_happy_path(self) -> None:
    self.reco_adapter.spotify_client.v1_audio_features.return_value = {
        'danceability': 1,
        'energy': 2,
        'key': 3,
        'loudness': 4,
        'mode': 5,
        'speechiness': 6,
        'acousticness': 7,
        'instrumentalness': 8,
        'liveness': 9,
        'valence': 10,
        'tempo': 11
    }
    self.reco_adapter.match_service_client.get_match.return_value = [
        MatchNeighbor('7C48cUjCGx14K5b41e9vTD', 1.0),
        MatchNeighbor('3x7gMvCsL1SS6THGwB55Pm', 2.0),
        MatchNeighbor('7sLQGgXFs4LaGAaDErPwOl', 5.0)
    ]

    recos_resp = self.reco_adapter.get_recos(track_id='id', size='5')

    self.assertEqual(200, recos_resp.response_code)

  def test_should_raise_httperror_when__validating_invalid_reco_size_type(
      self) -> None:
    self.assertRaises(HTTPError, self.reco_adapter.validate_reco_size, '1.1')

  def test_should_raise_httperror_when_validating_invalid_reco_size_value(
      self) -> None:
    self.assertRaises(HTTPError, self.reco_adapter.validate_reco_size, '0')

  def test_should_not_raise_httperror_on_valid_reco_size(self) -> None:
    self.reco_adapter.validate_reco_size('5')

  def test_should_create_correct_v1_track_embeddings(self) -> None:
    audio_features = {
        'danceability': 1,
        'energy': 2,
        'key': 3,
        'loudness': 4,
        'mode': 5,
        'speechiness': 6,
        'acousticness': 7,
        'instrumentalness': 8,
        'liveness': 9,
        'valence': 10,
        'tempo': 11
    }
    embedding = self.reco_adapter.get_embedding(audio_features=audio_features)

    self.assertEqual(embedding, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

  def test_should_raise_error_when_v1_track_embedding_cannot_be_created(
      self) -> None:
    audio_features = {
        'danceability': 1,
        'energy': 2,
        'key': 3,
        'loudness': 4,
        'mode': 5,
        'speechiness': 6,
        'acousticness': 7,
        'instrumentalness': 8,
        'liveness': 9,
    }

    self.assertRaises(KeyError, self.reco_adapter.get_embedding, audio_features)

  def test_should_properly_create_v1_playlist_tracks_payload(self) -> None:
    recos_response = {
        'recos': [{
            'id': '4JnCD65HeEbeTumgu6xEl3'
        }, {
            'id': '0iCxoVGB01iGIBgyFgovyt'
        }],
        'request': {
            'size': '2',
            'track': {
                'id': '2TRu7dMps7cVKOyazkj9Fb'
            }
        }
    }

    payload = self.reco_adapter.get_v1_playlist_tracks_payload(
        recos_response=recos_response)

    self.assertIsNotNone(payload)
    uris = payload['uris']
    self.assertIsNotNone(uris)
    self.assertEqual(2, len(uris))
    self.assertEqual('spotify:track:4JnCD65HeEbeTumgu6xEl3', uris[0])
    self.assertEqual('spotify:track:0iCxoVGB01iGIBgyFgovyt', uris[1])

  def test_should_properly_create_v1_playlist_on_happy_path(self) -> None:
    self.reco_adapter.spotify_client.v1_audio_features.return_value = {
        'danceability': 1,
        'energy': 2,
        'key': 3,
        'loudness': 4,
        'mode': 5,
        'speechiness': 6,
        'acousticness': 7,
        'instrumentalness': 8,
        'liveness': 9,
        'valence': 10,
        'tempo': 11
    }
    self.reco_adapter.match_service_client.get_match.return_value = [
        MatchNeighbor('7C48cUjCGx14K5b41e9vTD', 1.0),
        MatchNeighbor('3x7gMvCsL1SS6THGwB55Pm', 2.0),
        MatchNeighbor('7sLQGgXFs4LaGAaDErPwOl', 5.0)
    ]
    self.reco_adapter.spotify_client.v1_create_playlist.return_value = {
        'id': 'playlist_id'
    }

    create_playlist_response = self.reco_adapter.create_playlist(
        user_id='user_id',
        track_id='track_id',
        user_token='user_token',
        size='2')

    self.assertEqual(201, create_playlist_response.response_code)

  def test_should_raise_httperror_for_v1_playlist_on_get_recos_failure(
      self) -> None:
    self.assertRaises(HTTPError, self.reco_adapter.create_playlist, 'user_id',
                      'track_id', 'user_token', '0')

  def test_should_raise_httperror_for_v1_playlist_on_missing_authentication(
      self) -> None:
    self.reco_adapter.spotify_client.v1_audio_features.return_value = {
        'danceability': 1,
        'energy': 2,
        'key': 3,
        'loudness': 4,
        'mode': 5,
        'speechiness': 6,
        'acousticness': 7,
        'instrumentalness': 8,
        'liveness': 9,
        'valence': 10,
        'tempo': 11
    }
    self.reco_adapter.match_service_client.get_match.return_value = [
        MatchNeighbor('7C48cUjCGx14K5b41e9vTD', 1.0),
        MatchNeighbor('3x7gMvCsL1SS6THGwB55Pm', 2.0),
        MatchNeighbor('7sLQGgXFs4LaGAaDErPwOl', 5.0)
    ]

    def effect(user_id, user_token):
      raise HTTPError(url='url', code=401, msg='msg', hdrs=None, fp=None)

    self.reco_adapter.spotify_client.v1_create_playlist.side_effect = effect

    self.assertRaises(HTTPError, self.reco_adapter.create_playlist, 'user_id',
                      'track_id', 'user_token', '2')
