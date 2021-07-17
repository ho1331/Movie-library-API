from flask import request
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from src.models.genres import Genre
from src.tools.logging import loging


class GenresList(Resource):
    def post(self):
        """
        ---
        post:
          produces: application/json
          parameters:
           - in: body
             name: create genre
             description: Form to add genre
             schema:
               type: object
               properties:
                genre:
                 type: string
                 description: some genre


        responses:
          200:
            description:  New Genre
            schema:
              id: Genre
              properties:
                id:
                    type: integer
                    description: The genre's id
                genre:
                    type: string
                    description: The name of genre
        """

        request_json = request.get_json(cache=True)
        try:
            genres = Genre.create(
                request_json.get("genre"),
            )
            loging.debug(request_json, "SUCCESS: Created genre with parametrs")
        except IntegrityError as exc:
            loging.exept(f"ERROR: bad arguments in request")
            Genre.rollback()
            genres = {"Some errors": str(exc)}

        return genres, 200

    def get(self):
        """
        ---
        responses:
          200:
            description: List of genres
            schema:
              id: Genre
              properties:
                id:
                    type: integer
                    description: The genre's id
                genre:
                    type: string
                    description: The name of the user
        """
        genres = Genre.query.all()
        serialized_data = [{"id": genre.id, "genre": genre.genre} for genre in genres]
        return serialized_data, 200
