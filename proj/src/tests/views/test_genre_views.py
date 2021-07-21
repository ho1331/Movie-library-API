from random import randint

import pytest
from src.tests.mark_parametrize import authorizate_user, current_user


def test_genre_list__get(test_client):
    response = test_client.get("/api/genres/")
    assert response.status_code == 200


def test_genre_post(test_client):
    seed = str(randint(0, 3000))

    response = test_client.post("/api/genres/", json=dict(genre=seed))
    assert response.status_code == 401

    test_client.post(
        "/api/login/",
        json=dict(
            login=current_user.get("email"), password=authorizate_user["password"]
        ),
    )
    response = test_client.post("/api/genres/", json=dict(genre=seed))
    assert response.status_code == 201
