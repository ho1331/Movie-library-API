from flask import jsonify, request
from flask_login import \
    login_required  # decorator для ограничения доступа к методу
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from src.app import db
from src.models.directors import Director
##
from src.models.films import Film, Ref
from src.models.genres import Genre
from src.models.users import User


class FilmsList(Resource):
    @login_required
    def post(self):
        request_json = request.get_json(silent=True)
        try:
            film = Film.create(request_json)
        except IntegrityError as exc:
            Film.rollback()
            film = {"Some errors": str(exc)}

        return film, 200

    def get(self):
        """
        takes all films
        """
        films = Film.query.all()
        serialized_data = [
            {
                "id": film.id,
                "title": film.title,
                "release": str(film.release),
                "director_id": film.director_id,
                "description": film.description,
                "reting": film.reting,
                "poster": film.poster,
                "user_id": film.user_id,
            }
            for film in films
        ]
        return serialized_data, 200


class FilmsListViews(Resource):
    def get(self):
        """
        takes all users
        """
        # films = Film.query.join(Film.genres).all()
        # filtr by id diredctor
        #     films = Film.query.filter(Film.director_id == 2)
        films = (
            db.session.query(Film, Director, User.nick_name)
            .join(Director)
            .join(User)
            .all()
        )
        serialized_data = [
            {
                "title": film[0].title,
                "release": str(film[0].release),
                "director": f"{film[1].name} {film[1].sername}",
                "description": film[0].description,
                "reting": film[0].reting,
                "poster": film[0].poster,
                "user": film.nick_name,
            }
            for film in films
        ]
        return serialized_data, 200


class RefList(Resource):
    def post(self):
        request_json = request.get_json(silent=True)
        try:
            ref = Ref.create(request_json)
        except IntegrityError as exc:
            Ref.rollback()
            ref = {"Some errors": str(exc)}
        return ref, 200

    def get(self):
        """
        takes all users
        """
        refs = Ref.query.all()
        serialized_data = [
            {
                "films_id": ref.films_id,
                "genres_id": ref.genres_id,
            }
            for ref in refs
        ]
        return serialized_data, 200
