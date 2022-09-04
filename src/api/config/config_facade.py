import flask

class ConfigFacade():
    def __init__(self) -> None:
        self.environment = flask.current_app.config['ENVIRONMENT']
        self.match_service_enabled = flask.current_app.config['MATCH_SERVICE_ENABLED']
    
    def get_environment(self) -> str:
        return self.environment
    
    def is_match_service_enabled(self) -> bool:
        return self.match_service_enabled or False
