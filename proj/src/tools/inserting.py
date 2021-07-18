from random import randint, uniform

from faker import Factory
from sqlalchemy.exc import IntegrityError
from src.app import app, db
from src.models.directors import Director
from src.models.films import Film
from src.models.genres import Genre
from src.models.ref_genre_film import Ref
from src.models.users import User


@app.cli.command("seed_db")
def after_create():
    faker = Factory.create()
    count = 0
    while count <= 50:
        User.create(
            {
                "name": faker.first_name(),
                "nick_name": f"{faker.last_name_nonbinary()}{faker.suffix()}{faker.prefix()}",
                "email": faker.email(),
                "password": faker.password(),
            }
        )
        count += 1

    count = 0
    while count < 4:
        g_lst = ["anime", "horror", "comedy", "action"]
        Genre.create(genre=g_lst[count])
        count += 1

    count = 0
    while count <= 30:
        Director.create({"name": faker.first_name(), "sername": faker.last_name()})
        count += 1

    count_dierctors = Director.query.order_by(Director.id.desc()).first()
    count_users = User.query.order_by(User.id.desc()).first()

    count = 0
    while count <= 150:
        try:
            film = Film(
                title=faker.currency_name(),
                release=faker.date(),
                director_id=randint(1, int(count_dierctors.id)),
                description=faker.paragraph(
                    nb_sentences=5, variable_nb_sentences=False
                ),
                rating=round(uniform(1, 10), 2),
                poster=faker.image_url(),
                user_id=randint(1, int(count_users.id)),
            )
        except IntegrityError:
            film.rollback()
            count -= 1
        film.save()
        count += 1

    count_films = Film.query.order_by(Film.id.desc()).first()
    count_genres = Genre.query.order_by(Genre.id.desc()).first()
    count = 0
    while count <= 150:
        try:
            Ref.create(
                {
                    "films_id": randint(1, int(count_films.id)),
                    "genres_id": randint(1, int(count_genres.id)),
                }
            )
        except IntegrityError:
            Ref.rollback()
            count -= 1
        count += 1
    films = set(db.session.query(Film.id).all())
    genres = set(db.session.query(Ref.films_id).all())
    replace = films.difference(genres)
    for i in replace:
        push = {"films_id": i[0], "genres_id": 2}
        Ref.create(push)
