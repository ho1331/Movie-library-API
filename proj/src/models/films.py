from datetime import date, datetime
from os import name

from sqlalchemy.exc import IntegrityError
from src.app import db
from src.models.base import BaseModel


class Film(db.Model, BaseModel):
    """
    class Film
    """

    __tablename__ = "films"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(100), unique=False, nullable=False)
    genre_id = db.Column(
        db.Integer, db.ForeignKey("genres.id", ondelete="CASCADE"), nullable=False
    )
    release = db.Column(db.Date, unique=False, nullable=False)
    director_id = db.Column(db.Integer, db.ForeignKey("directors.id"), nullable=False)
    description = db.Column(db.String, default="description", nullable=False)
    reting = db.Column(
        db.Float,
        db.CheckConstraint("1 <= reting <= 10"),
        nullable=False,
    )
    poster = db.Column(db.String(255), unique=True, nullable=False)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    def __init__(
        self,
        title: str,
        genre_id: int,
        release: datetime,
        director_id: int,
        description: str,
        reting: float,
        poster: str,
        user_id: int,
    ) -> None:
        self.title = title
        self.genre_id = genre_id
        self.release = release
        self.director_id = director_id
        self.description = description
        self.reting = reting
        self.poster = poster
        self.user_id = user_id

    @staticmethod
    def create(data: dict) -> dict:
        """
        create user
        """
        result: dict = {}
        try:
            film = Film(**data)
            film.save()
            result = {
                "title": film.title,
                "genre_id": film.genre_id,
                "release": film.release,
                "director_id": film.director_id,
                "description": film.description,
                "reting": film.reting,
                "poster": film.poster,
                "user_id": film.user_id,
            }

        except IntegrityError as exc:
            Film.rollback()
            result = {"Some errors": str(exc)}

        return result
