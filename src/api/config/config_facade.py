import json
import src.api.util.env as env

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
        self._config = None

    def get_environment(self) -> str:
        return self.config['ENVIRONMENT']
    
    def is_match_service_enabled(self) -> bool:
        return self.config['MATCH_SERVICE_ENABLED'] or False
    
    def get_spotify_auth_client_config(self) -> bool:
        return self.config['SPOTIFY_AUTH_CLIENT_CONFIG'] or {}
    
    def get_spotify_client_config(self) -> bool:
        return self.config['SPOTIFY_CLIENT_CONFIG'] or {}
    
    @property
    def config(self) -> dict:
        if not self._config:
            config_default = load_config('default')
            config_environment = load_config(env.env_util.get_environment_variable('ENVIRONMENT'))
            # https://peps.python.org/pep-0448/
            config = {**config_default, **config_environment}
            self._config = config
        
        return self._config