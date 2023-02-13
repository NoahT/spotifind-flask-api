""" Unit test module for spotify_auth_client. """
import unittest
import requests
import src.api.clients.spotify_auth_client.client as spotify_auth_client
from google_crc32c import Checksum
from google.cloud.secretmanager import SecretManagerServiceClient
from unittest.mock import Mock, patch


class SpotifyAuthClientTestSuite(unittest.TestCase):
  """ Unit test suite for SpotifyAuthClient. """

  @patch('src.api.util.env.environment_variable_proxy.EnvironmentVariableProxy')
  def setUp(self, environment_variable_proxy) -> None:
    get_env = environment_variable_proxy.get_environment_variable
    get_env.side_effect = lambda key: {
        'PROJECT_ID': '841506577075',
        'CLIENT_ID': '081f994d972f46519c1c8f9f6f11102a',
        'SECRET_ID': 'spotify-rest-api-secret',
        'SECRET_VERSION_ID': 'latest',
        'PROJECT_NAME': 'spotifind-api'
    }[key]

    config_facade = Mock()
    config_facade.get_spotify_auth_client_config.return_value = {
        'CONNECT_TIMEOUT': 0.500,
        'READ_TIMEOUT': 1.000
    }
    self._spotify_auth_client = spotify_auth_client.SpotifyAuthClient(
        config_facade)
    self._response = requests.Response()

  @patch('google_crc32c.Checksum')
  @patch('google.cloud.secretmanager.SecretManagerServiceClient')
  def test_should_raise_error_for_4xx_response(
      self, secret_client: SecretManagerServiceClient, checksum: Checksum):
    secret_client.secret_version_path.return_value = 'path'
    version = Mock()
    version.payload.data.decode.return_value = 'secret_version'
    version.payload.data_crc32c.return_value = 1
    checksum.return_value.hexdigest.return_value = f'{1:08x}'.encode('ascii')
    secret_client.return_value.access_secret_version.return_value = version

    self._response.status_code = 400
    requests.post = Mock(return_value=self._response)

    self.assertRaises(requests.HTTPError,
                      self._spotify_auth_client.get_bearer_token)

  @patch('google_crc32c.Checksum')
  @patch('google.cloud.secretmanager.SecretManagerServiceClient')
  def test_should_raise_error_for_5xx_response(
      self, secret_client: SecretManagerServiceClient, checksum: Checksum):
    secret_client.secret_version_path.return_value = 'path'
    version = Mock()
    version.payload.data.decode.return_value = 'secret_version'
    version.payload.data_crc32c.return_value = 1
    checksum.return_value.hexdigest.return_value = f'{1:08x}'.encode('ascii')
    secret_client.return_value.access_secret_version.return_value = version

    self._response.status_code = 500
    requests.post = Mock(return_value=self._response)

    self.assertRaises(requests.HTTPError,
                      self._spotify_auth_client.get_bearer_token)

  def test_should_set_correct_headers(self):
    headers = self._spotify_auth_client.get_headers('Bearer basic_auth')

    self.assertEqual(
        headers, {
            'Authorization': 'Bearer basic_auth',
            'Content-Type': 'application/x-www-form-urlencoded'
        })

  def test_should_set_correct_urlencoded_form(self):
    form_urlencoded = self._spotify_auth_client.get_form_encoded()

    self.assertEqual(form_urlencoded, {'grant_type': 'client_credentials'})
