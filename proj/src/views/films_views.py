from flask import request
from flask_login import login_required  # decorator для ограничения доступа к методу
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from src.models.films import Film


class FilmsList(Resource):
    @login_required
    def post(self):
        request_json = request.get_json(cache=True)
        try:
            film = Film.create(request_json)
        except IntegrityError as exc:
            Film.rollback()
            film = {"Some errors": str(exc)}

        return film, 200

    def get(self):
        """
        takes all users
        """
        films = Film.query.all()
        serialized_data = [
            {
                "id": film.id,
                "title": film.title,
                "genre_id": film.genre_id,
                "release": str(film.release),
                "director_id": film.director_id,
                "description": film.description,
                "reting": film.reting,
                "poster": film.poster,
                "user_id": film.user_id,
            }
            for film in films
        ]
        return serialized_data, 200
