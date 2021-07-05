from faker import Factory
from flask_restful import Api

from src.app import app
from src.models.users import User
from src.views.directors_views import DirectorsList
from src.views.errors_views import Done, Errors
from src.views.films_views import FilmsList
from src.views.genres_views import GenresList
from src.views.login_views import LoginApi, LogoutApi
from src.views.users_views import Users, UsersList

# from sqlalchemy import event


# app = create_app()

# API route
api = Api(app)
api.add_resource(UsersList, "/api/users/")
api.add_resource(Users, "/api/users/<int:id>/")
api.add_resource(DirectorsList, "/api/directors/")
api.add_resource(GenresList, "/api/genres/")
api.add_resource(FilmsList, "/api/films/")
api.add_resource(Errors, "/api/error/")
api.add_resource(Done, "/api/done/")
api.add_resource(LoginApi, "/api/login/")
api.add_resource(LogoutApi, "/api/logout/")
# app.register_blueprint(sign, url_prefix="/api/login")

# command for inserting data into db tables
@app.cli.command("seed_db")
def after_create():
    faker = Factory.create()
    count = 0
    while count <= 1000:
        User.create(
            username=faker.first_name(),
            usernick=faker.last_name(),
            useremail=faker.email(),
            upass=faker.password(),
        )
        count += 1
