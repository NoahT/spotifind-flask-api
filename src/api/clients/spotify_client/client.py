from abc import ABC, abstractmethod
from ..spotify_auth_client.client import SpotifyAuthClient
from ..logging_client.client import LoggingClient
from ...config.config_facade import ConfigFacade
import json
import requests

class Client(ABC):
    @abstractmethod
    def v1_tracks(self, id, marketplace) -> dict:
        pass

    @abstractmethod
    def v1_audio_features(self, id) -> dict:
        pass

    @abstractmethod
    def v1_create_playlist(self, user_id, user_token, name='Spotifind playlist', description='https://github.com/NoahT/spotifind-flask-api', is_public=True) -> dict:
        pass

    @abstractmethod
    def v1_playlist_tracks(self, playlist_id, uris, user_token) -> dict:
        pass

class SpotifyClient(Client):
    def __init__(self, auth_client: SpotifyAuthClient, logging_client: LoggingClient, config_facade: ConfigFacade):
        self._hostname = 'https://api.spotify.com'
        self._v1_tracks_path = '/v1/tracks/'
        self._v1_audio_features_path = '/v1/audio-features/'
        self._v1_create_playlist_path = '/v1/users/{}/playlists'
        self._v1_playlist_tracks_path = '/v1/playlists/{}/tracks'
        self._auth_client = auth_client
        self._logger = logging_client.get_logger(self.__class__.__name__)
        self._config_facade = config_facade

    def v1_tracks(self, id, **kwargs) -> dict:
        batch = self._logger.batch()

        batch.log('Making GET call to {}'.format(self._v1_tracks_path), severity='INFO')
        batch.log('track_id={}'.format(id), severity='INFO')
        url = '{}{}{}'.format(self._hostname, self._v1_tracks_path, id)

        marketplace = kwargs.get('marketplace')

        if marketplace:
            batch.log('marketplace={}'.format(marketplace), severity='INFO')
            url = '{}?market={}'.format(url, marketplace)
        else:
            batch.log('marketplace query param omitted.', severity='INFO')

        bearer_token = self.get_bearer_token()

        headers = {
            'Authorization': bearer_token
        }

        response = requests.get(url, headers=headers, timeout=self.get_timeouts())
        batch.log('status={}'.format(response.status_code), severity='NOTICE')
        response.raise_for_status()
        response_json = response.json()
        batch.log('response={}'.format(response_json), severity='INFO')
        batch.commit()

        return response_json
    
    def v1_audio_features(self, id) -> dict:
        batch = self._logger.batch()

        batch.log('Making GET call to {}'.format(self.v1_audio_features), severity='INFO')
        batch.log('track_id={}'.format(id), severity='INFO')
        url = '{}{}{}'.format(self._hostname, self._v1_audio_features_path, id)

        bearer_token = self.get_bearer_token()

        headers = {
            'Authorization': bearer_token
        }

        response = requests.get(url, headers=headers, timeout=self.get_timeouts())
        batch.log('status={}'.format(response.status_code), severity='NOTICE')
        response.raise_for_status()
        response_json = response.json()
        batch.log('response={}'.format(response_json), severity='INFO')
        batch.commit()

        return response_json
    
    def v1_create_playlist(self, user_id, user_token, name='Spotifind playlist', description='https://github.com/NoahT/spotifind-flask-api', is_public=True) -> dict:
        batch = self._logger.batch()

        playlist_resource = self._v1_create_playlist_path.format(user_id)
        url = '{}{}'.format(self._hostname, playlist_resource)

        batch.log('Making POST call to {}'.format(playlist_resource), severity='INFO')
        batch.log('user_id={}'.format(user_id), severity='INFO')
        
        
        payload = {
            'name': name,
            'description': description,
            'public': is_public
        }
        batch.log('payload={}'.format(json.dumps(payload)), severity='INFO')

        headers = {
            'Authorization': user_token
        }

        response = requests.post(url, headers=headers, timeout=self.get_timeouts(), json=json.loads(json.dumps(payload)))
        batch.log('status={}'.format(response.status_code), severity='NOTICE')
        response.raise_for_status()
        response_json = response.json()
        batch.log('response={}'.format(response_json), severity='INFO')
        batch.commit()

        return response_json
    
    def v1_playlist_tracks(self, playlist_id, uris, user_token) -> dict:
        batch = self._logger.batch()

        playlist_resource = self._v1_playlist_tracks_path.format(playlist_id)
        url = '{}{}'.format(self._hostname, playlist_resource)
        
        batch.log('Making POST call to {}'.format(playlist_resource), severity='INFO')
        batch.log('playlist_id={}'.format(playlist_id), severity='INFO')

        payload = {
            'uris': ['spotify:track:{}'.format(uri) for uri in uris]
        }
        batch.log('payload={}'.format(json.dumps(payload)), severity='INFO')
        
        headers = {
            'Authorization': user_token
        }

        response = requests.post(url=url, json=payload, headers=headers)
        batch.log('status={}'.format(response.status_code), severity='NOTICE')
        response.raise_for_status()
        response_json = response.json()
        batch.log('response={}'.format(json.dumps(response_json)), severity='INFO')
        batch.commit()

        return response_json
    
    def get_timeouts(self) -> tuple:
        spotify_client_config = self._config_facade.get_spotify_client_config()
        read_timeout = spotify_client_config['READ_TIMEOUT']
        connect_timeout = spotify_client_config['CONNECT_TIMEOUT']

        return (connect_timeout, read_timeout)
    
    def get_bearer_token(self) -> str:
        bearer_token_json = self._auth_client.get_bearer_token()

        bearer_token = bearer_token_json['access_token']
        bearer_token = 'Bearer {}'.format(bearer_token)
        
        return bearer_token
