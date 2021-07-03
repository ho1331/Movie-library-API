from flask import request
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from src.models.genres import Genre


class GenresList(Resource):
    def post(self):
        request_json = request.get_json(cache=True)
        try:
            genres = Genre.create(
                request_json.get("genre"),
            )
        except IntegrityError as exc:
            Genre.rollback()
            genres = {"Some errors": str(exc)}

        return genres, 200

    def get(self):
        """
        takes all genres
        """
        genres = Genre.query.all()
        serialized_data = [{"id": genre.id, "genre": genre.genre} for genre in genres]
        return serialized_data, 200

    