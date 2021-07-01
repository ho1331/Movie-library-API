from flask_restful import Api

from src.app import create_app
from src.views.directors_views import DirectorsList
from src.views.films_views import FilmsList
from src.views.genres_views import GenresList
from src.views.users_views import Users, UsersList

app = create_app()

# API route
api = Api(app)
api.add_resource(UsersList, "/api/users/")
api.add_resource(Users, "/api/users/<int:id>/")
api.add_resource(DirectorsList, "/api/directors/")
api.add_resource(GenresList, "/api/genres/")
api.add_resource(FilmsList, "/api/films/")
