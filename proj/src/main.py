# from faker import Factory
from flask_restful import Api

from src.app import app

# inserting
from src.views.directors_views import DirectorsList
from src.views.films_views import FilmsList
from src.views.genres_views import GenresList
from src.views.login_views import sign
from src.views.users_views import Users, UsersList

# from sqlalchemy import event


# from src.models.users import User

# app = create_app()

# API route
api = Api(app)
api.add_resource(UsersList, "/api/users/")
api.add_resource(Users, "/api/users/<int:id>/")
api.add_resource(DirectorsList, "/api/directors/")
api.add_resource(GenresList, "/api/genres/")
api.add_resource(FilmsList, "/api/films/")
app.register_blueprint(sign, url_prefix="/api/login")


# @event.listens_for(User.__table__, "after_create")
# def after_create(mapper, connection, target):
#     table = User.__table__
#     faker = Factory.create()
#     connection.execute(
#         table.insert().values(
#             name=faker.first_name(),
#             nick_name=faker.last_name(),
#             email=faker.email(),
#             pswhash=hash(faker.password()),
#         )
#     )
