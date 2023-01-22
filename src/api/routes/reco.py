import json
import src.api.schemas as schemas
import src.api.util as util
from http import HTTPStatus
from flask import Blueprint, request

reco = Blueprint('reco', __name__)

@reco.route('/<id>', methods=['GET'])
def id(id):
    response = None
    size = request.args.get(key='size') or str(5)

    try:
        response = util.reco_adapter.get_recos(id=id, size=size)
    except Exception:
        response = schemas.response_builder_factory.get_builder(status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value).build_response(recos_response=None, id=id, size=size)
    finally:
        print(json.dumps(response.response))

    return response.response, response.response_code
