from flask import request
from flask_login.utils import current_user, login_required
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from src.models.directors import Director
from src.tools.logging import loging


class DirectorsList(Resource):
    def post(self):
        """
        ---
        post:
          produces: application/json
          parameters:
           - in: body
             name: create director
             description: Form to add director
             schema:
               type: object
               properties:
                dirname:
                    type: string
                    description: The name of director
                sername:
                    type: string
                    description: The sername of director


        responses:
          200:
            description:  New Director
            schema:
              id: Director
              properties:
                id:
                    type: integer
                    description: The director's id
                dirname:
                    type: string
                    description: The name of director
                sername:
                    type: string
                    description: The sername of director
        """

        request_json = request.get_json(cache=True)
        try:
            director = Director.create(
                request_json.get("dirname"),
                request_json.get("sername"),
            )
            loging.debug(request_json, "SUCCESS: Created director with parametrs")
        except IntegrityError as exc:
            loging.exept(f"ERROR: bad arguments in request")
            Director.rollback()
            director = {"Some errors": str(exc)}

        return director, 200

    def get(self):
        """
        ---
        responses:
          200:
            description: List of directors
            schema:
              id: Director
              properties:
                id:
                    type: integer
                    description: The director's id
                name:
                    type: string
                    description: The name of director
                sername:
                    type: string
                    description: The sername of director

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


class DirectorsItem(Resource):
    @login_required
    def delete(self, id):
        """
        ---
        delete:
          tags : directors
          parameters:
            - in: path
              name: id
              type: integer
              required: true
        responses:
            "400":
                description: "Invalid ID supplied"
            "404":
                description: "Director not found"
        """
        if current_user.is_admin == True:
            Director.query.filter(Director.id == id).delete()
            Director.commit()
            loging.info(id, "SUCCESS. Deleted director with id")
            return f"Director with id {id} is deleted.", 200
        loging.debug(
            "only admin",
            "FAIL. Not enough permissions to access",
        )
        return f"Not enough permissions to access", 200
