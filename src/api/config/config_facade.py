"""
  Config module with facade pattern to simplify access to only important
  fields. Supports environment-based configuration (development, staging, etc.)
"""
import json
from src.api.util import env

# Relative path: open(..) reads relative path based on current working
# directory which is not based on this location in source code (it will be based
# on path of execution for running process in Docker container)
CONFIG_PATH = './src/api/config/'


def load_config(config_env: str):
  config_file_path = f'{CONFIG_PATH}{config_env}.json'
  print(f'Config file: {config_file_path}')

  config = {}
  with open(config_file_path, 'r', encoding='utf-8') as file:
    config = json.loads(file.read())

  return config


class ConfigFacade():
  """ Facade class for config access. """

  def __init__(self) -> None:
    self._config = None

  def get_environment(self) -> str:
    return self.config['ENVIRONMENT']

  def is_match_service_enabled(self) -> bool:
    return self.config['MATCH_SERVICE_ENABLED'] or False

  def get_spotify_auth_client_config(self) -> dict:
    return self.config['SPOTIFY_AUTH_CLIENT_CONFIG'] or {}

  def get_spotify_client_config(self) -> dict:
    return self.config['SPOTIFY_CLIENT_CONFIG'] or {}

  def get_proxy_config(self) -> dict:
    return self.config['PROXY_CONFIG'] or {}

  @property
  def config(self) -> dict:
    if not self._config:
      config_default = load_config('default')
      config_environment = load_config(
          env.env_util.get_environment_variable('ENVIRONMENT'))
      # https://peps.python.org/pep-0448/
      config = {**config_default, **config_environment}
      self._config = config

    return self._config
