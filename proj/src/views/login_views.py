from flask import Blueprint, render_template, request
from flask_login import current_user, login_user
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from src.forms.loginform import LoginForm

sign = Blueprint("sign", __name__)


@sign.route("/")
def login():
    form = LoginForm()
    return render_template("login.html", title="Sign In", form=form)
