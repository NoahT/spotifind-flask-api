from flask import Flask, Blueprint
from .routes.reco import reco
from .routes.healthcheck import healthcheck
from flasgger import Swagger

v1 = Blueprint('name', __name__)
flask_app = Flask(__name__)

swagger = Swagger(flask_app)

v1.register_blueprint(reco, url_prefix='/reco')
flask_app.register_blueprint(v1, url_prefix='/v1')

# For health checks on Ingress load balancer in GCP
flask_app.register_blueprint(healthcheck)
