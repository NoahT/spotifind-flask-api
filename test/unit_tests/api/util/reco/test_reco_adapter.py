from http import HTTPStatus
from requests import HTTPError as ClientHTTPError, Response
from unittest.mock import patch, Mock
import src.api.util.reco.reco_adapter as reco_adapter
import src.api.schemas.response as response
import src.api.clients.matching_engine_client.match_service_pb2 as match_service
import unittest

class V1RecoAdapterTestSuite(unittest.TestCase):
    @patch('src.api.schemas.response.ResponseBuilderFactory')
    @patch('src.api.clients.matching_engine_client.client_aggregator.ClientAggregator')
    @patch('src.api.clients.logging_client.client.Client')
    @patch('src.api.clients.spotify_client.client.Client')
    def setUp(self, spotify_client, logging_client, client_aggregator, response_builder_factory) -> None:
        bad_request_response_builder = Mock(response.BadRequestResponseBuilder)
        bad_request_response_builder.build_response.return_value = {
            'status': 400
        }
        not_found_response_builder = Mock(response.NotFoundResponseBuilder)
        not_found_response_builder.build_response.return_value = {
            'status': 404
        }
        ok_response_builder = Mock(response.OkResponseBuilder)
        ok_response_builder.build_response.return_value = {
            'status': 200
        }
        self.bad_request_response_builder = bad_request_response_builder
        self.not_found_response_builder = not_found_response_builder
        self.ok_response_builder = ok_response_builder
        
        def response_builder_factory_side_effect(**kwargs):
            response_builder = None
            status_code = kwargs['status_code']
            if status_code == HTTPStatus.OK.value:
                response_builder = ok_response_builder
            elif status_code == HTTPStatus.NOT_FOUND.value:
                response_builder = not_found_response_builder
            else:
                response_builder = bad_request_response_builder
            
            return response_builder
        
        response_builder_factory.get_builder.side_effect = response_builder_factory_side_effect
        
        self.reco_adapter = reco_adapter.V1RecoAdapter(spotify_client=spotify_client, logging_client=logging_client, client_aggregator=client_aggregator, response_builder_factory=response_builder_factory)
    
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
        self.reco_adapter.match_service_client.get_match.return_value = match_service.MatchResponse()

        response = self.reco_adapter.get_recos(id='id', size='5')

        self.assertEqual(200, response['status'])

    def test_should_return_400_response_on_invalid_track_id(self) -> None:
        def side_effect(id):
            response = Mock(Response)
            response.status_code = 400
            raise ClientHTTPError(response=response)
        self.reco_adapter.spotify_client.v1_audio_features.side_effect = side_effect

        response = self.reco_adapter.get_recos(id='id', size='5')

        self.assertEqual(400, response['status'])

    def test_should_return_400_response_on_invalid_reco_size_value(self) -> None:
        response = self.reco_adapter.get_recos(id='id', size='0')
        
        self.assertEqual(400, response['status'])
    
    def test_should_return_400_response_on_invalid_reco_size_type(self) -> None:
        response = self.reco_adapter.get_recos(id='id', size='1.1')
        
        self.assertEqual(400, response['status'])

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

        self.assertEqual(embedding, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])

    def test_should_raise_error_when_v1_track_embedding_cannot_be_created(self) -> None:
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
        }
        
        self.assertRaises(KeyError, self.reco_adapter.get_embedding, audio_features)
