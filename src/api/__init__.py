from flask import Flask, Blueprint
from .routes.reco import reco

v1 = Blueprint('name', __name__)

flask_app = Flask(__name__)

v1.register_blueprint(reco, url_prefix='/reco')
flask_app.register_blueprint(v1, url_prefix='/v1')
