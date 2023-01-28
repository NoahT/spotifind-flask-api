from abc import ABC, abstractmethod
from http import HTTPStatus
from urllib.error import HTTPError
from requests import HTTPError as ClientHTTPError
import src.api.clients.spotify_client.client as spotify_client
import src.api.clients.logging_client.client as logging_client
import src.api.clients.matching_engine_client.client_aggregator as client_aggregator
import src.api.schemas.response as response

class RecoAdapter(ABC):
    @abstractmethod
    def get_recos(id: str, size: int) -> dict:
        pass

class V1RecoAdapter(RecoAdapter):
    def __init__(self, spotify_client: spotify_client.SpotifyClient, logging_client: logging_client.LoggingClient, client_aggregator: client_aggregator.ClientAggregator, response_builder_factory: response.ResponseBuilderFactory) -> None:
        self.spotify_client = spotify_client
        self.client_aggregator = client_aggregator
        self._match_service_client = None
        self.response_builder_factory = response_builder_factory
        # This is the feature space we chose for /v1/reco API. Note that these are the same features in Spotify /v1/audio-features API response
        self.feature_mapping = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence']
    
    def get_recos(self, id: str, size: str) -> response.Response:
        recos_response = None
        recos_dict = None
        try:
            self.validate_reco_size(size)
            size = int(size)

            audio_features = self.spotify_client.v1_audio_features(id=id)
            track_embedding = self.get_embedding(audio_features=audio_features)
            recos = self.match_service_client.get_match(match_request={'query': track_embedding, 'num_recos': (size + 1)})
            recos_response = self.response_builder_factory.get_builder(status_code=HTTPStatus.OK.value).build_response(recos_response=recos[0], id=id, size=int(size))
        except HTTPError as http_error:
            print(http_error.__str__())
            recos_response = self.response_builder_factory.get_builder(status_code=http_error.code).build_response(recos_response=recos_dict, id=id, size=size)
        except ClientHTTPError as client_http_error:
            print(client_http_error.__str__())
            recos_response = self.response_builder_factory.get_builder(status_code=client_http_error.response.status_code).build_response(recos_response=recos_dict, id=id, size=size)
        
        return recos_response
    
    def validate_reco_size(self, size: str) -> None:
        if not size.isdigit():
            raise HTTPError(None, HTTPStatus.BAD_REQUEST.value, 'Invalid size type.', None, None)
        if int(size) <= 0:
            raise HTTPError(None, HTTPStatus.BAD_REQUEST.value, 'Unable to handle non-positive reco size.', None, None)
    
    def get_embedding(self, audio_features: dict) -> list:
        embedding = []
        for feature in self.feature_mapping:
            feature_value = audio_features[feature]
            embedding.append(feature_value)
        
        return embedding
    
    @property
    def match_service_client(self):
        if not self._match_service_client:
            self._match_service_client = self.client_aggregator.get_client()
        
        return self._match_service_client