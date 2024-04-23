"""Runs the flask app."""

from os import environ

from dotenv import load_dotenv

from website import create_app

if __name__ == "__main__":

    load_dotenv()

    app = create_app(environ)
    app.run(debug=True)
