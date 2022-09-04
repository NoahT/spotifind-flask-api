from flask import Flask, Blueprint
from .routes.reco import reco
from .routes.healthcheck import healthcheck
from flasgger import Swagger
import json
import os

CONFIG_PATH = './config/'
def load_config(app: Flask, config_env: str):
    config_file = '{}{}.json'.format(CONFIG_PATH, config_env)
    print('Config file: {}'.format(config_file))
    app.config.from_file(config_file, load=json.load)

v1 = Blueprint('name', __name__)
flask_app = Flask(__name__)

load_config(flask_app, 'default')
config_env = os.environ['ENVIRONMENT']
load_config(flask_app, config_env)

swagger = Swagger(flask_app)

v1.register_blueprint(reco, url_prefix='/reco')
flask_app.register_blueprint(v1, url_prefix='/v1')

# For health checks on Ingress load balancer in GCP
flask_app.register_blueprint(healthcheck)
