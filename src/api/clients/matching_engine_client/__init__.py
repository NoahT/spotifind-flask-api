""" Initialization for match service client package. """
from .client_aggregator import ClientAggregator
from .client import MockMatchServiceClient, MatchServiceClient
from src.api.config import config

match_client_aggregator = ClientAggregator(config, MockMatchServiceClient,
                                           MatchServiceClient)
