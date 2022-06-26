from flask import Blueprint, request

reco = Blueprint('reco', __name__)

@reco.route('/<id>', methods=['GET'])
def v1_reco(id):
    print(id)
    print(request.args.get(key='size', type=int))
    return id
