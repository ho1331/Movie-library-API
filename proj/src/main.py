from flasgger import Swagger
from flask_restful import Api

from src.app import app
from src.tools.inserting import after_create
from src.views.directors_views import DirectorsItem, DirectorsList
from src.views.films_views import FilmsItem, FilmsList, FilmsListViews
from src.views.genres_views import GenresList
from src.views.login_views import LoginApi, LogoutApi
from src.views.users_views import Users, UsersList

# API route
api = Api(app)
swagger = Swagger(app)
api.add_resource(UsersList, "/api/users/")
api.add_resource(Users, "/api/users/<int:id>")
api.add_resource(DirectorsList, "/api/directors/")
api.add_resource(DirectorsItem, "/api/directors/<int:id>")
api.add_resource(GenresList, "/api/genres/")
api.add_resource(FilmsList, "/api/films/")
api.add_resource(FilmsListViews, "/api/films-views/")
api.add_resource(FilmsItem, "/api/films-views/<int:id>")
api.add_resource(LoginApi, "/api/login/")
api.add_resource(LogoutApi, "/api/logout/")
