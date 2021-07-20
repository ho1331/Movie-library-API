from random import randint, uniform

from faker import Factory
from src.main import api
from src.models.users import User

faker = Factory.create()


unauthorizate_user, authorizate_user = {
    "name": faker.first_name(),
    "nick_name": f"{faker.last_name_nonbinary()}{faker.suffix()}{faker.prefix()}",
    "email": faker.email(),
    "password": faker.password(),
}, {
    "name": faker.first_name(),
    "nick_name": f"{faker.last_name_nonbinary()}{faker.suffix()}{faker.prefix()}",
    "email": faker.email(),
    "password": faker.password(),
}


data_test_query = [
    (
        [faker.currency_name(), faker.currency_name()],
        round(uniform(1, 10), 2),
        faker.suffix(),
        randint(1, 20),
        [faker.date(), faker.date()],
        "asc",
        "desc",
    ),
    (
        [faker.currency_name(), faker.currency_name()],
        round(uniform(1, 10), 2),
        faker.suffix(),
        randint(1, 20),
        [faker.date(), faker.date()],
        "desc",
        "desc",
    ),
    (
        [faker.currency_name(), faker.currency_name()],
        round(uniform(1, 10), 2),
        faker.suffix(),
        randint(1, 20),
        [faker.date(), faker.date()],
        "asc",
        "asc",
    ),
]

data_test_film_crete = [
    (
        {
            "title": faker.currency_name(),
            "release": faker.date(),
            "director": [faker.first_name(), faker.last_name()],
            "description": faker.paragraph(nb_sentences=5, variable_nb_sentences=False),
            "rating": round(uniform(1, 10), 2),
            "poster": faker.image_url(),
            "genres": [faker.currency_name(), faker.currency_name()],
        },
        {
            "title": faker.currency_name(),
            "release": faker.currency_name(),
            "director": [faker.first_name(), faker.last_name()],
            "description": faker.paragraph(nb_sentences=5, variable_nb_sentences=False),
            "rating": round(uniform(1, 10), 2),
            "poster": faker.image_url(),
            "genres": [faker.currency_name(), faker.currency_name()],
        },
        {
            "title": faker.currency_name(),
            "release": faker.currency_name(),
            "director": [faker.first_name(), faker.last_name()],
            "description": faker.paragraph(nb_sentences=5, variable_nb_sentences=False),
            "rating": round(uniform(12, 15), 2),
            "poster": faker.image_url(),
            "genres": [faker.currency_name(), faker.currency_name()],
        },
    )
]

data_test_film_item_patch = [
    {
        "title": faker.currency_name(),
        "release": faker.date(),
        "director": [faker.name(), faker.last_name()],
        "description": faker.paragraph(nb_sentences=5, variable_nb_sentences=False),
        "rating": round(uniform(1, 10), 2),
        "poster": faker.image_url(),
        "genres": [faker.currency_name(), faker.currency_name()],
    }
]


data_test_film_item_del = [randint(1,50) for i in range(3)]


def create_user():
    """create mock current_user"""
    with api.app.app_context():
        return User.create(authorizate_user)


current_user = create_user()
