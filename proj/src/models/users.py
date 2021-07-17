"""User model"""
from datetime import datetime

from flask_login import UserMixin
from src.app import db, login
from src.models.base import BaseModel
from werkzeug.security import check_password_hash, generate_password_hash


class User(db.Model, BaseModel, UserMixin):
    """
    class USER
    """

    __tablename__ = "users"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(30), unique=False, nullable=False)
    nick_name = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    pswhash = db.Column(db.String(100), unique=True, nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    films = db.relationship("Film", backref="users", lazy=True)

    def __init__(
        self,
        name: str,
        nick_name: str,
        email: str,
        password: str,
        is_admin: bool = False,
    ) -> None:
        self.name = name
        self.nick_name = nick_name
        self.email = email
        self.pswhash = password
        self.is_admin = is_admin

    @staticmethod
    def create(data: dict) -> dict:
        """
        create user
        """
        user = User(**data)
        result = {
            "name": user.name,
            "nick_name": user.nick_name,
            "email": user.email,
            "password": user.set_password(user.pswhash),
            "is_admin": user.is_admin,
        }
        user.save()

        return result

    def set_password(self, password):
        """
        set hash password
        """
        self.pswhash = generate_password_hash(password, method="sha256")
        return self.pswhash

    def check_password(self, password):
        """
        check password
        """
        return check_password_hash(self.pswhash, password)

    # get users with id
    @staticmethod
    @login.user_loader
    def load_user(id):
        """
        add user to session place
        """
        return User.query.get(int(id))
