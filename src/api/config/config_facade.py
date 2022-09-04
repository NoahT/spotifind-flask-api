import flask

class ConfigFacade():
    def __init__(self) -> None:
        flask_app = flask.current_app
        self.config = flask_app.config
    
    def get_environment(self) -> str:
        return self.config['ENVIRONMENT']
    
    def is_match_service_enabled(self) -> bool:
        return self.config['MATCH_SERVICE_ENABLED'] or False