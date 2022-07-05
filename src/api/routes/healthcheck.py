from flask import Blueprint

healthcheck = Blueprint('healthcheck', __name__)

@healthcheck.route('/health', methods=['GET'])
def health():
    return ':)'

