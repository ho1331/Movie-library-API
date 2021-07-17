from logging import log

from flask import redirect, request
from flask_login import current_user, login_required, login_user, logout_user
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from src.models.users import User
from src.tools.logging import loging


class LoginApi(Resource):
    def post(self):
        body = request.get_json()
        user = User.query.filter_by(email=body.get("login")).first()
        if not user:
            loging.debug(body.get("login"), "FAIL: Invalid email")
            return {"error": "Invalid email"}, 401
        authorized = user.check_password(body.get("password"))
        if not authorized:
            loging.debug(body.get("password"), "FAIL: Invalid password")
            return {"error": "Invalid password"}, 401

        login_user(user, remember=True)
        loging.info(user.nick_name, "SUCCESS: Login with nick_name")
        return redirect("/api/done/")

    def get(self):
        if current_user.is_authenticated:
            return redirect("/api/done/")
        # here will be sign(registration) form
        form = {"login": "", "password": ""}
        return form, 200


class LogoutApi(Resource):
    @login_required
    def get(self):
        loging.info(current_user.nick_name, "User was logout with nick_name")
        logout_user()
        return redirect("/api/done/")
