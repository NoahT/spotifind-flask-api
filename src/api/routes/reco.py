from http import HTTPStatus
from flask import Blueprint, request
from ..config.config_facade import ConfigFacade
from ..clients.matching_engine_client.client_aggregator import ClientAggregator
from ..clients.matching_engine_client.client import MockMatchServiceClient, MatchServiceClient
from ..clients.spotify_client.client import SpotifyClient
from ..clients.spotify_auth_client.client import SpotifyAuthClient
from ..clients.logging_client.client import LoggingClient
from ..schemas.response import ResponseBuilderFactory
from ..util.reco_adapter import V1RecoAdapter

reco = Blueprint('reco', __name__)

response_builder_factory = ResponseBuilderFactory()

config_facade = ConfigFacade()
print('Environment: {}'.format(config_facade.get_environment()))
print('Is match service enabled: {}'.format(config_facade.is_match_service_enabled()))

logging_client = LoggingClient()
spotify_auth_client = SpotifyAuthClient(logging_client=logging_client)
spotify_client = SpotifyClient(auth_client=spotify_auth_client, logging_client=logging_client)
client_aggregator = ClientAggregator(config_facade=config_facade, mock_match_service_client=MockMatchServiceClient, match_service_client=MatchServiceClient)
reco_adapter = V1RecoAdapter(spotify_client=spotify_client, logging_client=logging_client, client_aggregator=client_aggregator, response_builder_factory=response_builder_factory)

@reco.route('/<id>', methods=['GET'])
def id(id):
    response = None
    size = request.args.get(key='size') or str(5)

    try:
        response = reco_adapter.get_recos(id=id, size=size)
    except Exception:
        response = response_builder_factory.get_builder(status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value).build_response(recos_response=None, id=id, size=size)
    finally:
        print(response.__str__())

    return response.response, response.response_code
