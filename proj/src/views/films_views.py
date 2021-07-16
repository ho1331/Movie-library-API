from flask import request
from flask_login import login_required  # decorator для ограничения доступа к методу
from flask_login import current_user
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from src.app import db
from src.models.directors import Director

##
from src.models.films import Film
from src.models.genres import Genre


class FilmsList(Resource):
    @login_required
    def post(self):
        """
        ---
        post:
          produces: application/json
          parameters:
           - in: body
             name: add new film
             description: add film to list by user
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

        """

        request_json = request.get_json(silent=True)
        try:
            film = Film.create(request_json)
        except IntegrityError as exc:
            Film.rollback()
            film = {"Some errors": str(exc)}

        return film, 200

    def get(self):
        """
        ---
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
        # paginate
        per_page = 10
        paginate = request.args.get("per_page")
        if paginate:
            per_page = paginate
        # partial match search
        part = request.args.get("part_title")
        # filters_params
        rating = request.args.get("rating")
        director_id = request.args.get("director-id")
        genres = request.args.get("genres")
        period = request.args.getlist("period")
        # sort_params
        sort_by_rating = request.args.get("sort-by-rating")
        sort_by_release = request.args.get("sort-by-release")
        # filters
        if part:
            films = (
                Film.query.filter(Film.title.like(f"%{part}%"))
                .paginate(per_page=int(per_page), error_out=False)
                .items
            )
        elif rating:
            films = Film.query.filter_by(rating=rating)
        elif director_id:
            films = Film.query.filter_by(director_id=director_id)
        elif period:
            films = (
                Film.query.filter(Film.release.between(period[0], period[1]))
                .paginate(per_page=int(per_page), error_out=False)
                .items
            )
        elif genres:
            films = (
                Film.query.filter(Film.genres.any(Genre.genre.in_([genres])))
                .paginate(per_page=int(per_page), error_out=False)
                .items
            )
        # sort
        elif sort_by_rating:
            films = (
                {
                    sort_by_rating == "asc": Film.query.order_by(Film.rating.asc()),
                    sort_by_rating == "desc": Film.query.order_by(Film.rating.desc()),
                }[True]
                .paginate(per_page=int(per_page), error_out=False)
                .items
            )
        elif sort_by_release:
            films = (
                {
                    sort_by_release == "asc": Film.query.order_by(Film.release.asc()),
                    sort_by_release == "desc": Film.query.order_by(Film.release.desc()),
                }[True]
                .paginate(per_page=int(per_page), error_out=False)
                .items
            )
        else:
            films = Film.query.paginate(per_page=int(per_page), error_out=False).items

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


class FilmsItem(Resource):
    @login_required
    def patch(self, id):
        request_json = request.get_json(silent=True)
        director = request_json.pop("director", None)
        request_genre = request_json.pop("genres", None)
        film = db.session.query(Film).get(id)
        if current_user.id == film.user_id or current_user.is_admin == True:
            Film.query.filter_by(id=id).update(request_json)
            # relation update director
            if director:
                Film.query.filter_by(id=id).update(
                    {
                        "director_id": Film.get_or_crete(
                            Director, name=director[0], sername=director[1]
                        ).id
                    }
                )
            # relation update genre
            if request_genre:
                film.genres = []
                for genre in request_genre:
                    # check if Genre is already exist
                    new_genre = Film.get_or_crete(Genre, genre=genre)
                    film.genres.append(new_genre)

            db.session.commit()
            return f"Success. Film with id={id} was updated", 200
        return f"Not enough permissions to access", 200

    @login_required
    def delete(self, id):
        """
        ---
        delete:
          tags : films
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
        if current_user.is_admin == True:
            Film.query.filter(Film.id == id).delete()
            Film.commit()
            return f"Quote with id {id} is deleted.", 200
        return f"Not enough permissions to access", 200
