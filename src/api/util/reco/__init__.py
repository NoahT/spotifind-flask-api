import src.api.clients.logging_client as logging_client
import src.api.clients.spotify_client as spotify_client
import src.api.clients.matching_engine_client as matching_engine_client
import src.api.schemas as schemas
from .reco_adapter import V1RecoAdapter

v1_reco_adapter = V1RecoAdapter(spotify_client.spotify_client, logging_client.logging_client, matching_engine_client.match_client_aggregator, schemas.response_builder_factory)
