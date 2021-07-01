from flask import request
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from src.models.directors import Director


class DirectorsList(Resource):
    def post(self):
        request_json = request.get_json(cache=True)
        try:
            director = Director.create(
                request_json.get("dirname"),
                request_json.get("sername"),
            )
        except IntegrityError as exc:
            Director.rollback()
            director = {"Some errors": str(exc)}

        return director, 200

    def get(self):
        """
        takes all directors
        """
        directors = Director.query.all()
        serialized_data = [
            {
                "id": director.id,
                "name": director.name,
                "sername": director.sername,
            }
            for director in directors
        ]
        return serialized_data, 200
