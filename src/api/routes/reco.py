from flask import Blueprint, request, jsonify
from flasgger import swag_from
from ..config.config_facade import ConfigFacade
from ..clients.matching_engine_client.client_aggregator import ClientAggregator
from ..clients.matching_engine_client.client import MockMatchServiceClient, MatchServiceClient

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
    config_facade = ConfigFacade()
    print('Environment: {}'.format(config_facade.get_environment()))
    print('Match service enabled: {}'.format(config_facade.is_match_service_enabled()))
    
    client_aggregator = ClientAggregator(config_facade=config_facade, mock_match_service_client=MockMatchServiceClient, match_service_client=MatchServiceClient)
    client = client_aggregator.get_client()
    match = client.get_match(match_request={})
    print(match.__str__())

    return jsonify({
        "request": {
            "track": {
                "id": id
            },
            "size": request.args.get(key='size', type=int) or 5
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
    })
