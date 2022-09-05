from http import HTTPStatus
from flask import Blueprint, request
from flasgger import swag_from
from ..config.config_facade import ConfigFacade
from ..clients.matching_engine_client.client_aggregator import ClientAggregator
from ..clients.matching_engine_client.client import MockMatchServiceClient, MatchServiceClient
from ..clients.spotify_client.client import SpotifyClient
from ..clients.spotify_auth_client.client import SpotifyAuthClient
from ..clients.logging_client.client import LoggingClient
from ..schemas.response import ResponseBuilderFactory
from ..util.reco_adapter import V1RecoAdapter

reco = Blueprint('reco', __name__)

@reco.route('/<id>', methods=['GET'])
@swag_from({
    "parameters": [
        {
            "name": "size",
            "in": "query",
            "type": "int",
            "required": False,
            "default": "5"
        },
        {
            "name": "id",
            "in": "path",
            "type": "string",
            "required": True
        }
    ],
    "definitions": {
        "response": {
            "type": "object",
            "properties": {
                "request": {
                    "$ref": "#/definitions/request_200"
                },
                "recos": {
                    "type": "array",
                    "items": {
                        "$ref": "#/definitions/track"
                    }
                }
            }
        },
        "request_200": {
            "description": "/id 200 response",
            "type": "object",
            "properties": {
                "track": {
                    "$ref": "#/definitions/track"
                },
                "size": {
                    "type": "integer"
                }
            }
        },
        "request_4xx": {
            "description": "/id 4xx response",
            "type": "object",
            "properties": {
                "status": {
                    "type": "integer"
                },
                "message": {
                    "type": "string"
                }
            }
        },
        "track": {
            "description": "Model object for Spotify track metadata",
            "type": "object",
            "properties": {
                "id": {
                    "type": "string"
                }
            }
        }
    },
    "responses": {
        "200": {
            "description": "A list of track ids.",
            "schema": {
                "$ref": "#/definitions/response"
            },
            "examples": {
                "Happy path": {
                    "summary": "Happy path/valid track id",
                    "value": {
                        "request": {
                            "track": {
                                "id": "62BGM9bNkNcvOh13B4wOyr"
                            },
                            "size": 5
                        },
                        "recos": [
                            {
                                "id": "2TRu7dMps7cVKOyazkj9Fb"
                            },
                            {
                                "id": "0bqrFwY1HixfnusFxhYbDl"
                            },
                            {
                                "id": "4BHSjbYylfOH5WAGusDyni"
                            },
                            {
                                "id": "3s9f1LQ6607eDj9UYCzmgk"
                            },
                            {
                                "id": "2HbKqm4o0w5wEeEFXm2sD4"
                            },
                        ]
                    }
                }
            }
        }
    }
})
def id(id):
    response = None

    response_builder_factory = ResponseBuilderFactory()
    try:
        config_facade = ConfigFacade()
        print('Environment: {}'.format(config_facade.get_environment()))
        print('Is match service enabled: {}'.format(config_facade.is_match_service_enabled()))

        logging_client = LoggingClient()
        spotify_auth_client = SpotifyAuthClient(logging_client=logging_client)
        spotify_client = SpotifyClient(auth_client=spotify_auth_client, logging_client=logging_client)
        client_aggregator = ClientAggregator(config_facade=config_facade, mock_match_service_client=MockMatchServiceClient, match_service_client=MatchServiceClient)
        reco_adapter = V1RecoAdapter(spotify_client=spotify_client, logging_client=logging_client, client_aggregator=client_aggregator, response_builder_factory=response_builder_factory)
        
        size = request.args.get(key='size') or str(5)
        
        response = reco_adapter.get_recos(id=id, size=size)
    except Exception as exception:
        response = response_builder_factory.get_builder(status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value).build_response(recos_response=None, id=id, size=size)
    finally:
        print(response.__str__())

    return response.response, response.response_code
