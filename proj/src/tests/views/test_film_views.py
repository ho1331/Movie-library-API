from random import randint

import pytest
from src.models.films import Film
from src.tests.data_to_test import (authorizate_user, current_user,
                                    data_test_film_crete,
                                    data_test_film_item_del,
                                    data_test_film_item_patch, data_test_query)


@pytest.mark.parametrize(
    "genre,rating,part_title,director_id,period,sort_by_rating,sort_by_release",
    data_test_query,
)
def test_film_list_views_get(
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


@pytest.mark.parametrize(
    "genre,rating,part_title,director_id,period,sort_by_rating,sort_by_release",
    data_test_query,
)
def test_film_list_views_all_filters_get(
    test_client,
    genre,
    rating,
    part_title,
    director_id,
    period,
    sort_by_rating,
    sort_by_release,
):
    response = test_client.get(
        "/api/films-views/",
        query_string={
            "genres": genre,
            "rating": rating,
            "part_title": part_title,
            "director-id": director_id,
            "period": period,
            "sort-by-rating": sort_by_rating,
        },
    )
    assert response.status_code == 200


@pytest.mark.parametrize(
    "curent_film, uncurent_args1,uncurent_args2",
    data_test_film_crete,
)
def test_film_list_post(test_client, curent_film, uncurent_args1, uncurent_args2):
    # if not login
    response = test_client.post("/api/films/", json=curent_film)
    assert response.status_code == 401

    # if login
    test_client.post(
        "/api/login/",
        json=dict(
            login=current_user.get("email"), password=authorizate_user["password"]
        ),
    )
    response = test_client.post("/api/films/", json=curent_film)
    assert response.status_code == 201

    # bad args
    response = test_client.post("/api/films/", json=uncurent_args1)
    assert response.status_code == 400
    response = test_client.post("/api/films/", json=uncurent_args2)
    assert response.status_code == 400


@pytest.mark.parametrize(
    "patch_data",
    data_test_film_item_patch,
)
def test_film_list_patch(test_client, patch_data):
    count_films = Film.query.order_by(Film.id.desc()).first()

    # if not login
    test_client.get("/api/logout/")
    response = test_client.patch(
        f"/api/films-views/{int(count_films.id)}", json=patch_data
    )
    assert response.status_code == 401

    # if  login
    test_client.post(
        "/api/login/",
        json=dict(
            login=current_user.get("email"), password=authorizate_user["password"]
        ),
    )

    response = test_client.patch(
        f"/api/films-views/{int(count_films.id)}", json=data_test_film_crete[0]
    )
    assert response.status_code == 400

    response = test_client.patch(f"/api/films-views/{int(count_films.id)+1}")
    assert response.status_code == 404

    response = test_client.patch(
        f"/api/films-views/{int(count_films.id)}", json=patch_data
    )
    assert response.status_code == 201


def test_film_list_del(test_client):
    count_films = Film.query.order_by(Film.id.desc()).first()
    # if not login
    test_client.get("/api/logout/")
    response = test_client.delete(f"/api/films-views/{randint(1,20)}")
    assert response.status_code == 401

    # if  login
    test_client.post(
        "/api/login/",
        json=dict(
            login=current_user.get("email"), password=authorizate_user["password"]
        ),
    )
    # not user_id==film_id
    response = test_client.delete(f"/api/films-views/{randint(1,20)}")
    assert response.status_code == 403

    response = test_client.delete(f"/api/films-views/{int(count_films.id)}")
    assert response.status_code == 200
