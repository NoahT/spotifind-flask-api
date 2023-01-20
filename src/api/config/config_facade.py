import json
import os

CONFIG_PATH = './config/'
def load_config(config_env: str):
    config_file_path = '{}{}.json'.format(CONFIG_PATH, config_env)
    print('Config file: {}'.format(config_file_path))
    
    config = {}
    with open(config_file_path, 'r', encoding='utf-8') as file:
        config = json.loads(file.read())
    
    return config

class ConfigFacade():
    def __init__(self) -> None:
        config_default = load_config('default')
        config_environment = load_config(os.environ['ENVIRONMENT'])
        # https://peps.python.org/pep-0448/
        config = {**config_default, **config_environment}
        
        self.environment = config['ENVIRONMENT']
        self.match_service_enabled = config['MATCH_SERVICE_ENABLED']
        self.spotify_auth_client_config = config['SPOTIFY_AUTH_CLIENT_CONFIG']
        self.spotify_client_config = config['SPOTIFY_CLIENT_CONFIG']
    
    def get_environment(self) -> str:
        return self.environment
    
    def is_match_service_enabled(self) -> bool:
        return self.match_service_enabled or False
    
    def get_spotify_auth_client_config(self) -> bool:
        return self.spotify_auth_client_config or {}
    
    def get_spotify_client_config(self) -> bool:
        return self.spotify_client_config or {}
