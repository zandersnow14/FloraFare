"""Initialises the flask app."""

from os import _Environ

from flask import Flask


def create_app(config: _Environ):
    """Configures the flask app."""

    app = Flask(__name__)
    app.config['SECRET_KEY'] = config['SECRET_KEY']

    return app
