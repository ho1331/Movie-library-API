from flask_restful import Resource
from flask import request
from sqlalchemy.exc import IntegrityError
from src.models.films import Ref

class RefList(Resource):
    def post(self):
        request_json = request.get_json(silent=True)
        try:
            ref = Ref.create(request_json)
        except IntegrityError as exc:
            Ref.rollback()
            ref = {"Some errors": str(exc)}
        return ref, 200

    def get(self):
        """
        ---
        responses:
          200:
            description: Ref list
            schema:
              id: Ref
              properties:
                id:
                    type: integer
                    description: ref id
                films_id:
                    type: integer
                    description: film's id
                genres_id:
                    type: integer
                    description: genre's id


        """
        refs = Ref.query.all()
        serialized_data = [
            {
                "films_id": ref.films_id,
                "genres_id": ref.genres_id,
            }
            for ref in refs
        ]
        return serialized_data, 200
