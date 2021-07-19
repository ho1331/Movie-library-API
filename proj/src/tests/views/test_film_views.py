from random import randint, uniform

import pytest
from faker import Factory

faker = Factory.create()

variants = [
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


@pytest.mark.parametrize(
    "genre,rating,part_title,director_id,period,sort_by_rating,sort_by_release",
    variants,
)
def test_film_list_views(
    test_client,
    genre,
    rating,
    part_title,
    director_id,
    period,
    sort_by_rating,
    sort_by_release,
):
    response1 = test_client.get("/api/films-views/", query_string={"genres": genre})
    response2 = test_client.get("/api/films-views/", query_string={"rating": rating})
    response3 = test_client.get(
        "/api/films-views/", query_string={"part_title": part_title}
    )
    response4 = test_client.get(
        "/api/films-views/", query_string={"director-id": director_id}
    )
    response5 = test_client.get("/api/films-views/", query_string={"period": period})
    response6 = test_client.get(
        "/api/films-views/", query_string={"sort-by-rating": sort_by_rating}
    )
    response7 = test_client.get(
        "/api/films-views/", query_string={"sort-by-release": sort_by_release}
    )

    assert response1.status_code == 200
    assert response2.status_code == 200
    assert response3.status_code == 200
    assert response4.status_code == 200
    assert response5.status_code == 200
    assert response6.status_code == 200
    assert response7.status_code == 200
