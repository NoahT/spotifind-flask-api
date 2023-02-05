""" Module for creating application instance and Blueprints for routing. """
from flask import Flask, Blueprint
from .routes.healthcheck import healthcheck
from src.api.routes import reco, playlist, healthcheck


def load_blueprints(app: Flask):
  v1 = Blueprint('name', __name__)

  v1.register_blueprint(reco, url_prefix='/reco')
  v1.register_blueprint(playlist, url_prefix='/playlist')
  app.register_blueprint(v1, url_prefix='/v1')

  # For health checks on Ingress load balancer in GCP
  app.register_blueprint(healthcheck)


flask_app = Flask(__name__)
flask_app.app_context().push()

load_blueprints(flask_app)
