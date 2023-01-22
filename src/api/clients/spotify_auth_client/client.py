from abc import ABC, abstractmethod
from google.cloud import secretmanager
from cachetools import cached
from cachetools import TTLCache
import google_crc32c
import requests
import base64
import src.api.util.env as env
import src.api.clients.logging_client.client as logging_client
import src.api.config.config_facade as config_facade

class Client(ABC):
    @abstractmethod
    def get_bearer_token(self) -> dict:
        pass

class SpotifyAuthClient(Client):
    def __init__(self, logging_client: logging_client.LoggingClient, config_facade: config_facade.ConfigFacade):
        self._hostname = 'https://accounts.spotify.com'
        self._api_token_path = '/api/token'
        self._config_facade = config_facade

    def get_bearer_token(self) -> dict:
        token = self.get_bearer_token_from_cache(key='public')
        return token
    
    @cached(cache=TTLCache(maxsize=1, ttl=3600))
    def get_bearer_token_from_cache(self, key='public') -> dict:
        # By default public scope is only scope we can use for client credentials. When we look into adding a
        # resource for creating playlists we will need to use a new authentication flow that propagates a token
        # with the correct authorization scope in the request headers
        endpoint = '{}{}'.format(self._hostname, self._api_token_path)
        basic_token = self.get_basic_token()
        basic_auth = 'Basic {}'.format(basic_token)

        form_urlencoded = self.get_form_encoded()

        headers = self.get_headers(basic_auth)

        response = requests.post(endpoint, headers=headers, data=form_urlencoded, timeout=self.get_timeouts())
        response.raise_for_status()
        response_json = response.json()

        return response_json
    
    def get_timeouts(self) -> tuple:
        spotify_auth_client_config = self._config_facade.get_spotify_auth_client_config()
        read_timeout = spotify_auth_client_config['READ_TIMEOUT']
        connect_timeout = spotify_auth_client_config['CONNECT_TIMEOUT']

        return (connect_timeout, read_timeout)

    def get_basic_token(self) -> str:
        secret = self.access_secret_version()
        credentials = '{}:{}'.format(self._client_id, secret)
        credentials = credentials.encode('utf-8')
        basic_token = base64.b64encode(credentials)
        basic_token = str(basic_token, 'utf-8')
        
        return basic_token
    
    def get_form_encoded(self) -> dict:
        form_urlencoded = {
            'grant_type': 'client_credentials'
        }

        return form_urlencoded
    
    def get_headers(self, basic_auth: str) -> dict:
        headers =  {
            'Authorization': basic_auth,
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        return headers
    
    def access_secret_version(self):
        client = secretmanager.SecretManagerServiceClient()
        name = client.secret_version_path(self._project_id, self._secret_id, self._secret_version_id)

        response = client.access_secret_version(request={'name': name})

        crc32c = google_crc32c.Checksum()
        crc32c.update(response.payload.data)
        if response.payload.data_crc32c != int(crc32c.hexdigest(), 16):
            self.logger.log('Data corruption detected.', severity='WARNING')
            return response

        payload = response.payload.data.decode('UTF-8')

        return payload
    
    @property
    def project_id(self) -> str:
        if not self._project_id:
            self._project_id = env.env_util.get_environment_variable('PROJECT_ID')
        
        return self._project_id
    
    @property
    def client_id(self) -> str:
        if not self._client_id:
            self._client_id = env.env_util.get_environment_variable('CLIENT_ID')
        
        return self._client_id
    
    @property
    def secret_id(self) -> str:
        if not self._secret_id:
            self._secret_id = env.env_util.get_environment_variable('SECRET_ID')
        
        return self._secret_id
    
    @property
    def secret_version_id(self) -> str:
        if not self._secret_version_id:
            self._secret_version_id = env.env_util.get_environment_variable('SECRET_VERSION_ID')
        
        return self._secret_version_id
