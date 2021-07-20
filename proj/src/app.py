"""basic app params"""
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from src.config import Config

db = SQLAlchemy()


def create_app():
    """
    create app params
    """
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    Migrate(app, db, directory="src/models/migrations")
    return app


app = create_app()
login = LoginManager(app)
