from datetime import datetime

# import bcrypt
from app import db


class User(db.Model):
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

    # def set_password(self, pw):
    #     pwhash = bcrypt.hashpw(pw.encode("utf8"), bcrypt.gensalt())
    #     self.pswhash = pwhash.decode("utf8")

    # def check_password(self, pw):
    #     if self.pswhash is not None:
    #         expected_hash = self.pswhash.encode("utf8")
    #         return bcrypt.checkpw(pw.encode("utf8"), expected_hash)
    #     return False

