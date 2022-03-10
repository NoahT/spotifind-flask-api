from flask import Flask
from flask import request
from flask.helpers import url_for
from markupsafe import escape

flask_app = Flask(__name__)

@flask_app.route('/', methods=['GET'])
def index():
    return 'Index page!'