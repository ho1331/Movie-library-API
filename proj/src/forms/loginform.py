from flask_wtf import Form
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import Required


class LoginForm(Form):
    username = StringField("Your username", validators=[Required()])
    password = PasswordField("Your password", validators=[Required()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")
