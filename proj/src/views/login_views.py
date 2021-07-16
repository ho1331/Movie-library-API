from flask import redirect, request
from flask_login import current_user, login_required, login_user, logout_user
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from src.models.users import User


class LoginApi(Resource):
    def post(self):
        body = request.get_json()
        user = User.query.filter_by(email=body.get("login")).first()
        if not user:
            return {"error": "Invalid email"}, 401
        authorized = user.check_password(body.get("password"))
        if not authorized:
            return {"error": "Invalid password"}, 401

        login_user(user, remember=True)
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
        logout_user()
        return redirect("/api/done/")


# sign = Blueprint("sign", __name__)


# @sign.route("/", methods=["GET", "POST"])
# def login():
#     form = LoginForm()
#     if current_user.is_authenticated:
#         return redirect("/api/films/")
#     if form.validate_on_submit():
#         user = User.query.filter_by(email=form.login.data).first()
#         if user is None or not user.check_password(form.password.data):
#             flash("Invalid username or password")
#             return redirect("/api/login/")
#         login_user(user, remember=form.remember_me.data)
#         return redirect("/api/films/")
#     return render_template("login.html", title="Sign In", form=form)


# @login_required
# @sign.route("/logout")
# def logout():
#     logout_user()
#     return redirect("/api/done/")
