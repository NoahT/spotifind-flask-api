from .client_aggregator import ClientAggregator
from .client import MockMatchServiceClient, MatchServiceClient
import src.api.config as config

match_client_aggregator = ClientAggregator(config.config_facade, MockMatchServiceClient, MatchServiceClient)