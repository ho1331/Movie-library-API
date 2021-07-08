from flask_restful import Api

from src.app import app
from src.data_to_insert.inserting import after_create
from src.views.directors_views import DirectorsList
from src.views.errors_views import Done, Errors
from src.views.films_views import FilmsList, FilmsListViews, RefList
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
api.add_resource(FilmsListViews, "/api/films-views/")
api.add_resource(Errors, "/api/error/")
api.add_resource(Done, "/api/done/")
api.add_resource(LoginApi, "/api/login/")
api.add_resource(LogoutApi, "/api/logout/")
api.add_resource(RefList, "/api/genre-film/")
# app.register_blueprint(sign, url_prefix="/api/login")

# command for inserting data into db tables
