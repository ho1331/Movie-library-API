"""module user views"""
from flask import request
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from src.models.users import User
from src.tools.logging import loging


class Users(Resource):
    """
    class Users
    """

    def get(self, id: int):
        """
        ---
        tags:
         - name: Users
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
                is_admin:
                    type: boolean
                    description: Show user's privilege

        """
        user = User.query.filter_by(id=id).first_or_404()
        serialized_data = {
            "id": user.id,
            "name": user.name,
            "nick_name": user.nick_name,
            "email": user.email,
            "password": user.pswhash,
            "date_created": str(user.created),
            "is_admin": user.is_admin,
        }
        return serialized_data, 200


class UsersList(Resource):
    def post(self):
        """
        ---
        tags:
         - name: Users
        post:
          produces: application/json
          parameters:
           - in: body
             name: create user
             description: Form to add User
             schema:
               type: object
               properties:
                name:
                    type: string
                    description: User's name
                nick_name:
                    type: string
                    description: User's nick name
                email:
                    type: string
                    description: User's email
                password:
                    type: string
                    description: User's password
                is_admin:
                    type: boolean
                    description: prev
                    requared: false
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
                password:
                    type: string
                    description: The users hash password
                created_at:
                    type: string
                    format: date-time
                    description: The period of user registration

        """
        request_json = request.get_json(silent=True)
        # client add new user
        try:
            user = User.create(request_json)
            loging.debug(request_json, "SUCCESS: Created user with parametrs")
        except (IntegrityError, TypeError, AssertionError) as exc:
            loging.exept("ERROR: bad arguments in request")
            User.rollback()
            return {"status": f"error: {str(exc)}"}, 400
        return user, 201

    def get(self):
        """
        ---
        tags:
         - name: Users
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
                password:
                    type: string
                    description: The users hash password
                created_at:
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
