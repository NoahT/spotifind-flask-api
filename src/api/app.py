""" Module for creating application instance and Blueprints for routing. """
from flask import Flask, Blueprint
from .routes.healthcheck import healthcheck
from src.api.routes import reco, playlist, healthcheck
from src.api.config import config
from werkzeug.middleware.proxy_fix import ProxyFix


def load_xff_proxy_configuration(app: Flask) -> None:
  proxy_config = config.get_proxy_config()

  if proxy_config['ENABLED']:
    limit_x_forwarded_for = proxy_config['LIMIT_X_FORWARDED_FOR']
    limit_x_forwarded_proto = proxy_config['LIMIT_X_FORWARDED_PROTO']
    limit_x_forwarded_host = proxy_config['LIMIT_X_FORWARDED_HOST']
    limit_x_forwarded_prefix = proxy_config['LIMIT_X_FORWARDED_PREFIX']

    app.wsgi_app = ProxyFix(app.wsgi_app,
                            x_for=limit_x_forwarded_for,
                            x_proto=limit_x_forwarded_proto,
                            x_host=limit_x_forwarded_host,
                            x_prefix=limit_x_forwarded_prefix)


def load_blueprints(app: Flask) -> None:
  v1 = Blueprint('name', __name__)

  v1.register_blueprint(reco, url_prefix='/reco')
  v1.register_blueprint(playlist, url_prefix='/playlist')
  app.register_blueprint(v1, url_prefix='/v1')

  # For health checks on Ingress load balancer in GCP
  app.register_blueprint(healthcheck)


flask_app = Flask(__name__)
flask_app.app_context().push()

load_xff_proxy_configuration(flask_app)
load_blueprints(flask_app)
