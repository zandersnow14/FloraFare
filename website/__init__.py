"""Initialises the flask app."""

from os import _Environ

from flask import Flask

from .views import views
from .auth import auth


def create_app(config: _Environ):
    """Configures the flask app."""

    app = Flask(__name__)
    app.config['SECRET_KEY'] = config['SECRET_KEY']

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    return app
