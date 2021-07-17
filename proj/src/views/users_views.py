from flask import request
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from src.models.users import User
from src.tools.logging import loging


class Users(Resource):
    def get(self, id: int):
        """
        ---
        parameters:
          - in: path
            name: id
            type: integer
            required: true
        responses:
          200:
            description: A single user item
            schema:
              id: User
              properties:
                id:
                    type: integer
                    description: The user's id
                name:
                    type: string
                    description: The name of the user
                nick_name:
                    type: string
                    description: The users nick_name
                email:
                    type: string
                    description: The users email (login)
                pswhash:
                    type: string
                    description: The users hash password
                created:
                    type: string
                    format: date-time
                    description: The period of user registration

        """
        user = User.query.filter_by(id=id).first_or_404()
        serialized_data = {
            "id": user.id,
            "name": user.name,
            "nick_name": user.nick_name,
            "email": user.email,
            "password": user.pswhash,
            "date_created": str(user.created),
        }
        return serialized_data, 200


class UsersList(Resource):
    def post(self):
        """
        ---
        post:
          produces: application/json
          parameters:
           - in: body
             name: create user
             description: Form to add User
             schema:
               type: object
               properties:
                username:
                 type: string
                 description: User's name
                usernick:
                 type: string
                 description: User's nick name
                useremail:
                 type: string
                 description: User's email
                upass:
                 type: string
                 description: User's password

        responses:
          200:
            description:  New User
            schema:
              id: User
              properties:
                id:
                    type: integer
                    description: The user's id
                name:
                    type: string
                    description: The name of the user
                nick_name:
                    type: string
                    description: The users nick_name
                email:
                    type: string
                    description: The users email (login)
                pswhash:
                    type: string
                    description: The users hash password
                created:
                    type: string
                    format: date-time
                    description: The period of user registration

        """
        request_json = request.get_json(silent=True)
        # client add new user
        try:
            user = User.create(request_json)
            loging.debug(request_json, "SUCCESS: Created user with parametrs")
        except IntegrityError as exc:
            loging.exept(f"ERROR: bad arguments in request")
            User.rollback()
            user = {"Bad args ERROR. Explanation": str(exc)}

        return user, 200

    def get(self):
        """
        ---
        responses:
          200:
            description: List of users
            schema:
              id: User
              properties:
                id:
                    type: integer
                    description: The user's id
                name:
                    type: string
                    description: The name of the user
                nick_name:
                    type: string
                    description: The users nick_name
                email:
                    type: string
                    description: The users email (login)
                pswhash:
                    type: string
                    description: The users hash password
                created:
                    type: string
                    format: date-time
                    description: The period of user registration

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
