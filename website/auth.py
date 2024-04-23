"""Authentication routes for the website."""

from flask import Blueprint

auth = Blueprint('auth', __name__)


@auth.route("/register")
def register():
    return "<h1>Register</h1>"


@auth.route("/login")
def login():
    return "<h1>Login</h1>"


@auth.route("logout")
def logout():
    return "<h1>Logout</h1>"
