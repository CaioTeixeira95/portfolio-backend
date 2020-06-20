from flask import Flask
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    CORS(app)

    from .message import bp_message
    app.register_blueprint(bp_message)

    return app
