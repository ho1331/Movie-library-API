"""Film model"""
from flask_login import current_user
from sqlalchemy.orm import validates
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
    release = db.Column(db.Date, unique=False, nullable=False, index=True)
    director_id = db.Column(
        db.Integer, db.ForeignKey("directors.id", ondelete="SET NULL"), nullable=True
    )
    description = db.Column(db.String, default="description", nullable=False)
    rating = db.Column(db.Float, nullable=False)
    poster = db.Column(db.String(255), unique=True, nullable=False)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    genres = db.relationship("Genre", secondary="ref", backref="films", lazy=True)

    @validates("rating")
    def validate_rating(self, key, field):
        """
        Check rating input
        """
        if 1 <= field <= 10:
            return field
        else:
            raise AssertionError("field 'rating should be between 1 and 10")

    @staticmethod
    def create(data: dict) -> dict:
        """
        create film
        """
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
        result = {
            "title": film.title,
            "release": str(film.release),
            "director": f"{new_director.name} {new_director.sername}",
            "description": film.description,
            "rating": film.rating,
            "poster": film.poster,
            "user": current_user._get_current_object().nick_name,
            "genre": [genres.genre for genres in film.genres],
        }
        return result

    @staticmethod
    def patch(id: int, film: object, data: dict) -> dict:
        """
        update film by id
        """
        director = data.pop("director", None)
        request_genre = data.pop("genres", None)
        Film.query.filter_by(id=id).update(data)
        # relation update director
        if director:
            Film.query.filter_by(id=id).update(
                {
                    "director_id": Film.get_or_crete(
                        Director, name=director[0], sername=director[1]
                    ).id
                }
            )
        # relation update genre
        if request_genre:
            film.genres = []
            for genre in request_genre:
                # check if Genre is already exist
                new_genre = Film.get_or_crete(Genre, genre=genre)
                film.genres.append(new_genre)

    @staticmethod
    def delete(id: int) -> None:
        """
        delete film by id
        """
        Film.query.filter(Film.id == id).delete()
        Film.commit()
