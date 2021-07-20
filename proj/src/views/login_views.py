from flask import redirect, request
from flask_login import current_user, login_required, login_user, logout_user
from flask_restful import Resource
from src.models.users import User
from src.tools.logging import loging


class LoginApi(Resource):
    def post(self):
        """
        ---
        tags:
         - name: Login
        post:
          produces: application/json
          parameters:
           - in: body
             name: login form
             description: Login users
             schema:
               type: object
               properties:
                login:
                    type: string
                    description: user's email
                password:
                    type: string
                    description: user's password


        responses:
          200:
            description:  Success
          400:
            description:  Invalid email/password
        """

        body = request.get_json(force=True)
        user = User.query.filter_by(email=body.get("login")).first()
        if not user:
            loging.debug(body.get("login"), "FAIL: Invalid email")
            return {"error": "Invalid email"}, 400
        authorized = user.check_password(body.get("password"))
        if not authorized:
            loging.debug(body.get("password"), "FAIL: Invalid password")
            return {"error": "Invalid password"}, 400

        login_user(user, remember=True)
        loging.info(user.nick_name, "SUCCESS: Login with nick_name")
        return {"status": "success"}, 200

    def get(self):
        if current_user.is_authenticated:
            return {"Info": "is_authenticated"}, 200
        # here will be sign(registration) form
        return {"login": "", "password": ""}, 200


class LogoutApi(Resource):
    @login_required
    def get(self):
        """
        ---
        tags:
         - name: Login
        responses:
          200:
            description:  Success
        """
        loging.info(current_user.nick_name, "User was logout with nick_name")
        logout_user()
        return {"status": "success"}, 200
