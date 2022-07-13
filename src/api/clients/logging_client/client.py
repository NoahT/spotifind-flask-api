from abc import ABC, abstractmethod
from google.cloud import logging_v2
import os

class Client(ABC):
    @abstractmethod
    def get_logger(self, name) -> logging_v2.Logger:
        pass

class LoggingClient(Client):
    def __init__(self) -> None:
        project_name = os.environ['PROJECT_NAME']
        self.client = logging_v2.Client(project=project_name)

    def get_logger(self, name) -> logging_v2.Logger:
        logger = self.client.logger(name=name)
        return logger
