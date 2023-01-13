import flask

class ConfigFacade():
    def __init__(self) -> None:
        app = flask.current_app
        with app.app_context():
            self.environment = flask.current_app.config['ENVIRONMENT']
            self.match_service_enabled = flask.current_app.config['MATCH_SERVICE_ENABLED']
            self.spotify_auth_client_config = flask.current_app.config['SPOTIFY_AUTH_CLIENT_CONFIG']
            self.spotify_client_config = flask.current_app.config['SPOTIFY_CLIENT_CONFIG']
    
    def get_environment(self) -> str:
        return self.environment
    
    def is_match_service_enabled(self) -> bool:
        return self.match_service_enabled or False
    
    def get_spotify_auth_client_config(self) -> bool:
        return self.spotify_auth_client_config or {}
    
    def get_spotify_client_config(self) -> bool:
        return self.spotify_client_config or {}
