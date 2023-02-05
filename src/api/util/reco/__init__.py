""" Initialization for recommendations utilities package. """
from src.api.clients import spotify_client
from src.api.clients import matching_engine_client
from src.api import schemas
from .reco_adapter import V1RecoAdapter
from .reco_controller import V1RecoController

v1_reco_adapter = V1RecoAdapter(spotify_client.spotify_client,
                                matching_engine_client.match_client_aggregator,
                                schemas.response_builder_factory)
v1_reco_controller = V1RecoController(v1_reco_adapter,
                                      schemas.response_builder_factory)
