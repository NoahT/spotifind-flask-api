from abc import ABC, abstractmethod
from http import HTTPStatus
from urllib.error import HTTPError
from requests import HTTPError as ClientHTTPError
from ..clients.spotify_client.client import Client as SpotifyClient
from ..clients.logging_client.client import Client as LoggingClient
from ..clients.matching_engine_client.client_aggregator import ClientAggregator
from ..schemas.response import ResponseBuilderFactory, Response
from google.protobuf.json_format import MessageToDict

class RecoAdapter(ABC):
    @abstractmethod
    def get_recos(id: str, size: int) -> dict:
        pass

class V1RecoAdapter(RecoAdapter):
    def __init__(self, spotify_client: SpotifyClient, logging_client: LoggingClient, client_aggregator: ClientAggregator, response_builder_factory: ResponseBuilderFactory) -> None:
        self.spotify_client = spotify_client
        self.match_service_client = client_aggregator.get_client()
        self.response_builder_factory = response_builder_factory
        # This is the feature space we chose for /v1/reco API. Note that these are the same features in Spotify /v1/audio-features API response
        self.feature_mapping = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']
    
    def get_recos(self, id: str, size: str) -> Response:
        recos_response = None
        recos_dict = None
        try:
            if not size.isdigit():
                raise HTTPError(None, HTTPStatus.BAD_REQUEST.value, 'Invalid size type.', None, None)
            size_int = int(size)
            if size_int <= 0:
                raise HTTPError(None, HTTPStatus.BAD_REQUEST.value, 'Unable to handle non-positive reco size.', None, None)
            
            audio_features = self.spotify_client.v1_audio_features(id=id)
            track_embedding = self.get_embedding(audio_features=audio_features)
            recos = self.match_service_client.get_match(match_request={'query': track_embedding, 'num_recos': size_int})
            recos_dict = MessageToDict(recos, including_default_value_fields=True, preserving_proto_field_name=False)
            recos_response = self.response_builder_factory.get_builder(status_code=HTTPStatus.OK.value).build_response(recos_response=recos_dict, id=id, size=size)
        except HTTPError as http_error:
            print(http_error.__str__())
            recos_response = self.response_builder_factory.get_builder(status_code=http_error.code).build_response(recos_response=recos_dict, id=id, size=size)
        except ClientHTTPError as client_http_error:
            print(client_http_error.__str__())
            recos_response = self.response_builder_factory.get_builder(status_code=client_http_error.response.status_code).build_response(recos_response=recos_dict, id=id, size=size)
        
        return recos_response
    
    def get_embedding(self, audio_features: dict) -> list:
        embedding = []
        for feature in self.feature_mapping:
            feature_value = audio_features[feature]
            embedding.append(feature_value)
        
        return embedding
