from datetime import datetime

from flask import Flask, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://postgres:postgres@localhost:5432/cars_api"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(30), unique=False, nullable=False)
    nick_name = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    pswhash = db.Column(db.String(60), unique=True, nullable=False)
    created = db.Column(db.DateTime, unique=True, nullable=False)

    def __init__(
        self, name: str, nick_name: str, email: str, pswhash: str, created: datetime
    ) -> None:
        self.name = name
        self.nick_name = nick_name
        self.email = email
        self.pswhash = pswhash
        self.created = created


if __name__ == "__main__":
    app.run(debug=True)
