from flask import request
from flask_login import current_user, login_required
from flask_restful import Resource
from sqlalchemy.exc import DataError, IntegrityError
from src.app import db
from src.models.films import Film
from src.models.genres import Genre
from src.tools.logging import loging


class FilmsList(Resource):
    @login_required
    def post(self):
        """
        ---
        tags:
         - name: Films
        post:
          produces: application/json
          parameters:
           - in: body
             name: add new film
             description: Views with id reference (for admin)
             schema:
               type: object
               properties:
                title:
                    type: string
                    description: Title of film
                release:
                    type: string
                    format: date
                    description: The date of film's release
                description:
                    type: string
                    description: film's description
                rating:
                    type: number
                    format: float
                    description: film's rating
                poster:
                    type: string
                    description: link to film's poster
                genre:
                    type: array
                    items:
                      type: string
                    minItems: 1
                director(name,sername):
                    type: array
                    items:
                      type: string
                    minItems: 2
                    maxItems: 2

        responses:
          200:
            description: New Film
            schema:
              id: Film
              properties:
                id:
                    type: integer
                    description: The film's id
                title:
                    type: string
                    description: Title of film
                release:
                    type: string
                    format: date
                    description: The date of film's release
                description:
                    type: string
                    description: film's description
                rating:
                    type: number
                    format: float
                    description: film's rating
                poster:
                    type: string
                    description: link to film's poster
                genre:
                    type: array
                    items:
                      type: string
                director(name,sername):
                    type: array
                    items:
                      type: string
                user_nick_name:
                    type: string
                    description: user nick_name by film

        """

        request_json = request.get_json(silent=True)
        try:
            film = Film.create(request_json)
            loging.debug(request_json, "SUCCESS: Created film with parametrs")
        except (IntegrityError, DataError, TypeError, AssertionError) as exc:
            loging.exept(f"ERROR: bad arguments in request")
            Film.rollback()
            return {"Bad args ERROR. Explanation": str(exc)}, 400

        return film, 201

    def get(self):
        """
        ---
        tags:
         - name: Films
        responses:
          200:
            description: List of films
            schema:
              id: Film
              properties:
                id:
                    type: integer
                    description: The film's id
                title:
                    type: string
                    description: Title of film
                release:
                    type: string
                    description: The date of film's release
                director_id:
                    type: integer
                    description: director id by film
                description:
                    type: string
                    description: film's description
                rating:
                    type: number
                    format: float
                    description: film's rating
                poster:
                    type: string
                    description: link to film's poster
                user_id:
                    type: integer
                    description: user id by film
                genre:
                    type: array
                    items:
                      type: integer

        """
        # films = Film.query.all()
        films = Film.query.all()
        serialized_data = [
            {
                "id": film.id,
                "title": film.title,
                "release": str(film.release),
                "director_id": film.director_id,
                "description": film.description,
                "rating": film.rating,
                "poster": film.poster,
                "user_id": film.user_id,
                "genres": [genre.id for genre in film.genres],
            }
            for film in films
        ]
        return serialized_data, 200


class FilmsListViews(Resource):
    def get(self):
        """
        ---
        tags:
         - name: Films
        parameters:
          - in: query
            name: director-id
            type: integer
            required: false
          - in: query
            name: genres
            required: false
            type: array
            items:
                type: string
            collectionFormat: multi
            minItems: 1
          - in: query
            name: period
            required: false
            type: array
            items:
                type: string
                format: date
            collectionFormat: multi
            minItems: 2
            maxItems: 2
          - in: query
            name: part_title
            description: partial search title of film
            required: false
          - in: query
            name: sort-by-rating
            description: sorting film by rating (asc/desc)
            schema:
                type: string
                enum: [asc, desc]
            required: false
          - in: query
            name: sort-by-release
            description: sorting film by date of release (asc/desc)
            schema:
                type: string
                enum: [asc, desc]
            required: false
          - in: query
            name: page
            type: integer
            description: asc or desc
            required: false
          - in: query
            name: per_page
            type: integer
            description: asc or desc
            required: false

        responses:
          404:
            description: "Film not found"
          200:
            description: List of films (for User views)
            properties:
            id:
                type: integer
                description: The film's id
            title:
                type: string
                description: Title of film
            release:
                type: string
                description: The date of film's release
            director_id:
                type: string
                description: directors info
            description:
                type: string
                description: film's description
            rating:
                type: number
                format: float
                description: film's rating
            poster:
                type: string
                description: link to film's poster
            user:
                type: string
                description: user nick

        """
        films = FilmsListViews.querys(request.args)
        serialized_data = [
            {
                "id": film.id,
                "title": film.title,
                "release": str(film.release),
                "director": f"{film.directors.name} {film.directors.sername}"
                if film.director_id
                else "unknown",
                "description": film.description,
                "rating": film.rating,
                "poster": film.poster,
                "user": film.users.nick_name,
                "genre": [genre.genre for genre in film.genres],
            }
            for film in films
        ]
        return serialized_data, 200

    @staticmethod
    def querys(data: dict) -> dict:
        params = data
        per_page = 10
        paginate = params.get("per_page")
        if paginate:
            per_page = paginate
        all = db.session.query(Film)
        for param in params:
            if param == "part_title":
                all = all.filter(Film.title.like(f"%{params.get(param).lower()}%"))
            if param == "rating":
                all = all.filter_by(rating=params.get(param))
            if param == "director-id":
                all = all.filter_by(director_id=params.get(param))
            if param == "period":
                period = request.args.getlist("period")
                all = all.filter(Film.release.between(period[0], period[1]))
            if param == "genres":
                all = all.filter(Film.genres.any(Genre.genre.in_([params.get(param)])))
            # sort
            if param == "sort-by-rating":
                all = {
                    params.get(param) == "asc": all.order_by(Film.rating.asc()),
                    params.get(param) == "desc": all.order_by(Film.rating.desc()),
                }[True]
            if param == "sort-by-release":
                all = {
                    params.get(param) == "asc": all.order_by(Film.release.asc()),
                    params.get(param) == "desc": all.order_by(Film.release.desc()),
                }[True]
        return all.paginate(per_page=int(per_page), error_out=False).items


class FilmsItem(Resource):
    @login_required
    def patch(self, id):
        request_json = request.get_json(silent=True)
        # director = request_json.pop("director", None)
        # request_genre = request_json.pop("genres", None)
        film = db.session.query(Film).get(id)
        if not film:
            return {"ERROR. NOT FOUND film_id": id}, 404

        # check update (only films created user or admin)
        if current_user.id == film.user_id or current_user.is_admin == True:
            try:
                Film.patch(id, film, request_json)
            except (IntegrityError, DataError, TypeError, AssertionError) as exc:
                loging.exept(f"ERROR: bad arguments in request")
                Film.rollback()
                return {"Bad args ERROR. Explanation": str(exc)}, 400

            db.session.commit()
            loging.info(id, "SUCCESS. Updated film with id")
            return {"Success": f"Film with id={id} was updated"}, 201
        loging.debug(id, "FAIL. Not enough permissions to access. BAD user_id")
        return {"permissions ERROR": "Not enough permissions to access"}, 403

    @login_required
    def delete(self, id):
        """
        ---
        tags:
         - name: Films
        delete:
          parameters:
            - in: path
              name: id
              type: integer
              required: true
        responses:
            "400":
                description: "Invalid ID supplied"
            "404":
                description: "Film not found"
        """

        film = db.session.query(Film).get(id)
        if not film:
            return {"ERROR. NOT FOUND film_id": id}, 404
        if current_user.id == film.user_id or current_user.is_admin == True:
            try:
                Film.delete(id)
                loging.info(id, "SUCCESS. Deleted film with id")
            except (IntegrityError, DataError, TypeError, AssertionError) as exc:
                loging.exept(f"ERROR: bad arguments in request")
                Film.rollback()
                return {"Bad args ERROR. Explanation": str(exc)}, 400
            return {"Success": f"Film with id {id} was deleted."}, 200
        loging.debug(
            f"{film.user_id} != {current_user.id}",
            "FAIL. Not enough permissions to access (explaine: film.user_id==user.id",
        )
        return {"permissions ERROR": "Not enough permissions to access"}, 403
