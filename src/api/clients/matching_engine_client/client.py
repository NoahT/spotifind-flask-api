from abc import ABC, abstractmethod

class Client(ABC):
    @abstractmethod
    def get_match(self, match_request: dict) -> dict:
        pass;

class MockMatchServiceClient(Client):
    def __init__(self) -> None:
        super().__init__()
    
    def get_match(self, match_request: dict) -> dict:
        return super().get_match(match_request)

class MatchServiceClient(Client):
    def __init__(self) -> None:
        super().__init__()
    
    def get_match(self, match_request: dict) -> dict:
        return super().get_match(match_request)