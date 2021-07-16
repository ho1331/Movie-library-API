from os import name

from flask_login import current_user
from sqlalchemy.exc import IntegrityError
from src.app import db
from src.models.base import BaseModel
from src.models.directors import Director
from src.models.genres import Genre


class Film(db.Model, BaseModel):
    """
    class Film
    """

    __tablename__ = "films"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(100), unique=False, nullable=False)
    release = db.Column(db.Date, unique=False, nullable=False)
    director_id = db.Column(db.Integer, db.ForeignKey("directors.id"), nullable=False)
    description = db.Column(db.String, default="description", nullable=False)
    rating = db.Column(
        db.Float,
        db.CheckConstraint("1 <= rating AND rating<= 10"),
        nullable=False,
    )
    poster = db.Column(db.String(255), unique=True, nullable=False)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    is_admin = db.Column(db.Boolean, default=False)
    genres = db.relationship("Genre", secondary="ref", backref="films", lazy=True)

    @staticmethod
    def create(data: dict) -> dict:
        """
        create user
        """
        result: dict = {}
        # pop genres to exec
        genr = data.pop("genres")
        # pop director to exec
        director = data.pop("director")

        film = Film(**data)
        # add directorin relationship table
        new_director = Film.get_or_crete(
            Director, name=director[0], sername=director[1]
        )
        film.director_id = new_director.id
        # add user_id by curent user
        film.user_id = current_user._get_current_object().id
        # add genre in relationship table
        for genre in genr:
            # check if Genre is already exist
            new_genre = Film.get_or_crete(Genre, genre=genre)
            film.genres.append(new_genre)
        film.save()
        try:
            result = {
                "title": film.title,
                "release": str(film.release),
                "director": f"{new_director.name} {new_director.sername}",
                "description": film.description,
                "rating": film.rating,
                "poster": film.poster,
                "user": current_user._get_current_object().nick_name,
                "genre": [genres.genre for genres in film.genres],
                "is_admin": film.is_admin,
            }
        except IntegrityError as exc:
            Film.rollback()
            result = {"Some errors": str(exc)}
        return result


class Ref(db.Model, BaseModel):
    """
    class condition Film and Genre
    """

    __tablename__ = "ref"
    __table_args__ = (db.PrimaryKeyConstraint("films_id", "genres_id"),)
    films_id = db.Column(
        db.Integer, db.ForeignKey("films.id", ondelete="CASCADE"), nullable=False
    )
    genres_id = db.Column(
        db.Integer, db.ForeignKey("genres.id", ondelete="CASCADE"), nullable=False
    )

    @staticmethod
    def create(data: dict) -> dict:
        """
        create ref
        """
        result: dict = {}
        ref = Ref(**data)
        ref.save()
        result = {
            "films_id": ref.films_id,
            "genres_id": ref.genres_id,
        }

        return result
