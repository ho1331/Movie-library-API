from flask import request
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from src.models.users import User


class Users(Resource):
    def get(self, id: int):
        user = User.get(id)
        return user, 200


class UsersList(Resource):
    def post(self):
        request_json = request.get_json(silent=True)
        # client add new user
        try:
            user = User.create(
                request_json.get("username"),
                request_json.get("usernick"),
                request_json.get("useremail"),
                request_json.get("upass"),
            )
        except IntegrityError as exc:
            User.rollback()
            user = {"Some errors": str(exc)}

        return user, 200

    def get(self):
        """
        takes all users
        """
        users = User.query.all()
        serialized_data = [
            {
                "id": user.id,
                "name": user.name,
                "nick_name": user.nick_name,
                "email": user.email,
                "password": user.pswhash,
                "date_created": str(user.created),
            }
            for user in users
        ]
        return serialized_data, 200
