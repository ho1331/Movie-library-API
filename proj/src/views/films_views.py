from flask import request
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from src.models.films import Film


class FilmsList(Resource):
    def post(self):
        request_json = request.get_json(cache=True)
        try:
            film = Film.create(
                request_json.get("ftitle"),
                request_json.get("fgenre_id"),
                request_json.get("frelease"),
                request_json.get("fdirector_id"),
                request_json.get("fdescription"),
                request_json.get("freting"),
                request_json.get("fposter"),
                request_json.get("fuser_id"),
            )
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
