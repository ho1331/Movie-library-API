from flask import request
from flask_login.utils import current_user, login_required
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from src.models.directors import Director
from src.tools.logging import loging


class DirectorsList(Resource):
    @login_required
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
            director = Director.create(request_json)
            loging.debug(request_json, "SUCCESS: Created director with parametrs")
        except IntegrityError as exc:
            loging.exept(f"ERROR: bad arguments in request")
            Director.rollback()
            director = {"Bad args ERROR. Explanation": str(exc)}

        return director, 201

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
            try:
                Director.delete(id)
                loging.info(id, "SUCCESS. Deleted director with id")
            except SQLAlchemyError as exp:
                return {"DELETE Error": f"{id} not FOUND, {exp}"}
            return {"Success": f"Director with id {id} is deleted."}, 404
        loging.debug(
            "only admin",
            "FAIL. Not enough permissions to access",
        )
        return {"permissions ERROR": "Not enough permissions to access"}, 403
