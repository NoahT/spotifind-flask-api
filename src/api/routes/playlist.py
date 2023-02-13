"""
  Playlist module. Contains relative URI(s) for creating playlist
  resources.
"""
from http import HTTPStatus
from flask import Blueprint, request, Response
from src.api import schemas
import src.api.util.reco as reco_util
import json
import traceback

playlist = Blueprint('playlist', __name__)


@playlist.route('/<user_id>/<track_id>', methods=['POST'])
def v1_playlist_user_id_track_id(user_id: str, track_id: str):
  print(request.headers)
  size = request.args.get(key='size') or str(5)
  user_token = request.headers['Authorization']

  response = None
  try:
    response = reco_util.v1_reco_controller.create_playlist(
        user_id=user_id, track_id=track_id, user_token=user_token, size=size)
  except Exception:  # pylint: disable=broad-exception-caught
    print(traceback.format_exc())
    response = schemas.response_builder_factory.get_builder(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value).build_response(
            recos_response=None, track_id=track_id, size=size)
  finally:
    print(json.dumps(response.response))
    print(response.response_code)

  flask_response = Response(response=response.response,
                            status=response.response_code,
                            headers=response.response_headers)

  return flask_response
