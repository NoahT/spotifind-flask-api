from flask import Flask, Blueprint
from .routes.healthcheck import healthcheck
from flasgger import Swagger
import json
import os

CONFIG_PATH = './config/'
def load_config(app: Flask, config_env: str):
    config_file = '{}{}.json'.format(CONFIG_PATH, config_env)
    print('Config file: {}'.format(config_file))
    app.config.from_file(config_file, load=json.load)

def load_blueprints(app: Flask):
    from .routes.reco import reco

    v1 = Blueprint('name', __name__)
    swagger = Swagger(app)

    v1.register_blueprint(reco, url_prefix='/reco')
    app.register_blueprint(v1, url_prefix='/v1')

    # For health checks on Ingress load balancer in GCP
    app.register_blueprint(healthcheck)

flask_app = Flask(__name__)
flask_app.app_context().push()

load_config(flask_app, 'default')
config_env = os.environ['ENVIRONMENT']
load_config(flask_app, config_env)

load_blueprints(flask_app)