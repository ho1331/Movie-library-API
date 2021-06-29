from datetime import datetime

from sqlalchemy.exc import IntegrityError

# import bcrypt
from src.app import db
from src.models.base import BaseModel


class User(db.Model, BaseModel):
    """
    class USER
    """

    __tablename__ = "users"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(30), unique=False, nullable=False)
    nick_name = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    pswhash = db.Column(db.String(60), unique=True, nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __init__(self, name: str, nick_name: str, email: str, pswhash: str) -> None:
        self.name = name
        self.nick_name = nick_name
        self.email = email
        self.pswhash = pswhash

    @staticmethod
    def create(username: str, usernick: str, useremail: str, upass: str) -> dict:
        """
        create user
        """
        result: dict = {}
        try:
            user = User(
                name=username, nick_name=usernick, email=useremail, pswhash=upass
            )
            result = {
                "name": user.name,
                "nick_name": user.nick_name,
                "email": user.email,
                "password": user.pswhash,
            }
            user.save()
        except IntegrityError as exc:
            User.rollback()
            result = {"Some errors": str(exc)}

        return result

    @staticmethod
    def get(id: int) -> dict:
        """
        Query a user by id
        """
        user = User.query.filter_by(id=id).first_or_404()
        return {
            "id": user.id,
            "name": user.name,
            "nick_name": user.nick_name,
            "email": user.email,
            "password": user.pswhash,
            "date_created": str(user.created),
        }

    # def set_password(self, pw):
    #     pwhash = bcrypt.hashpw(pw.encode("utf8"), bcrypt.gensalt())
    #     self.pswhash = pwhash.decode("utf8")

    # def check_password(self, pw):
    #     if self.pswhash is not None:
    #         expected_hash = self.pswhash.encode("utf8")
    #         return bcrypt.checkpw(pw.encode("utf8"), expected_hash)
    #     return False
