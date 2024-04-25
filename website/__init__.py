"""Initialises the flask app."""

from os import _Environ

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()


def create_app(config: _Environ):
    """Configures the flask app."""

    app = Flask(__name__)
    app.config['SECRET_KEY'] = config['SECRET_KEY']

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://zandersnow@localhost/flora_fare'
    db.init_app(app)

    from .models import User

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.filter_by(user_id=user_id).first()

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    return app
