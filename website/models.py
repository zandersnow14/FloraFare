"""Models for the database."""

from flask_login import UserMixin
from sqlalchemy import Column, Integer, String

from . import db


class User(db.Model, UserMixin):
    """Class to define a user."""

    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(25), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(60), nullable=False)

    def __init__(self, username: str, email: str, password: str) -> None:
        self.username = username
        self.email = email
        self.password = password

    def get_id(self):
        return str(self.user_id)


def register_user(self) -> None:
    user = User.query.filter(User.username == self.username).all()
