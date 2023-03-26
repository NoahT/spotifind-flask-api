"""
  Reco module. Contains relative URI(s) for getting recommendations
  in resource state.
"""
import json
import traceback
from src.api import schemas
import src.api.util.reco as reco_util
from http import HTTPStatus
from flask import Blueprint, request

reco = Blueprint('reco', __name__)


@reco.route('/<track_id>', methods=['GET'])
def v1_reco_track_id(track_id: str):
  response = None
  size = request.args.get(key='size') or str(5)
  verbose = request.args.get(key='verbose', type=bool) or False
  print(f'verbose={verbose}')

  try:
    response = reco_util.v1_reco_controller.get_recos(track_id, size, verbose)
  except Exception:  # pylint: disable=broad-exception-caught
    print(traceback.format_exc())
    response = schemas.response_builder_factory.get_builder(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value).build_response(
            recos_response=None, track_id=track_id, size=size, verbose=verbose)
  finally:
    print(json.dumps(response.response))

  return response.response, response.response_code
