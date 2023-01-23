from abc import ABC, abstractmethod
from google.cloud import logging_v2
import src.api.util.env as env

class Client(ABC):
    @abstractmethod
    def get_logger(self, name: str) -> logging_v2.Logger:
        pass

class LoggingClient(Client):
    def __init__(self) -> None:
        self._client = None

    def get_logger(self, name: str) -> logging_v2.Logger:
        logger = self.client.logger(name=name)
        return logger
    
    @property
    def project_name(self) -> str:
        return env.env_util.get_environment_variable('PROJECT_NAME')
    
    @property
    def client(self) -> logging_v2.Client:
        if not self._client:
            self._client = logging_v2.Client(project=self.project_name)
        
        return self._client