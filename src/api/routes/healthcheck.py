"""
  Healthcheck module. Contains resource for health checks on public cloud.
"""
from flask import Blueprint

healthcheck = Blueprint('healthcheck', __name__)


@healthcheck.route('/health', methods=['GET'])
def health():
  return ':)'
