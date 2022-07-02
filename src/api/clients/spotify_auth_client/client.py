from abc import ABC, abstractmethod
from google.cloud import secretmanager
import os
import requests
import base64

class Client(ABC):
    @abstractmethod
    def get_bearer_token(self) -> dict:
        pass

class SpotifyAuthClient(Client):
    def __init__(self):
        self._hostname = 'https://accounts.spotify.com'
        self._api_token_path = '/api/token'
        self._project_id = os.environ['PROJECT_ID']
        self._client_id = os.environ['CLIENT_ID']
        self._secret_id = os.environ['SECRET_ID']
        self._secret_version_id = os.environ['SECRET_VERSION_ID']

    def get_bearer_token(self) -> dict:
        endpoint = '{}{}'.format(self._hostname, self._api_token_path)
        basic_token = self.get_basic_token()
        basic_auth = 'Basic {}'.format(basic_token)

        form_urlencoded = self.get_form_encoded()

        headers = self.get_headers(basic_auth)

        response = requests.post(endpoint, headers=headers, data=form_urlencoded)
        response.raise_for_status()
        response_json = response.json()

        return response_json
    
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
    
    def get_headers(self, basic_auth) -> dict:
        headers =  {
            'Authorization': basic_auth,
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        return headers
    
    def access_secret_version(self):
        # Create the Secret Manager client.
        client = secretmanager.SecretManagerServiceClient()

        # Build the resource name of the secret version.
        name = f"projects/{self._project_id}/secrets/{self._secret_id}/versions/{self._version_id}"

        # Access the secret version.
        response = client.access_secret_version(request={"name": name})

        # Verify payload checksum.
        crc32c = google_crc32c.Checksum()
        crc32c.update(response.payload.data)
        if response.payload.data_crc32c != int(crc32c.hexdigest(), 16):
            print("Data corruption detected.")
            return response

        payload = response.payload.data.decode("UTF-8")

        return payload