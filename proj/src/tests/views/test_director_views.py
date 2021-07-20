from random import randint

import pytest
from src.tests.data_to_test import (
    admin,
    authorizate_user,
    current_user,
    data_admin,
    data_test_director_create,
)


def test_director_list__get(test_client):
    response = test_client.get("/api/directors/")
    assert response.status_code == 200


def test_director_post(test_client):

    response = test_client.post("/api/directors/", json=data_test_director_create[0])
    assert response.status_code == 401

    test_client.post(
        "/api/login/",
        json=dict(
            login=current_user.get("email"), password=authorizate_user["password"]
        ),
    )
    response = test_client.post("/api/directors/", json=data_test_director_create[0])
    assert response.status_code == 201


def test_director_del(test_client):
    # if not login
    test_client.get("/api/logout/")
    response = test_client.delete(f"/api/directors/{randint(1,30)}")
    assert response.status_code == 401

    # if  login user
    test_client.post(
        "/api/login/",
        json=dict(
            login=current_user.get("email"), password=authorizate_user["password"]
        ),
    )
    response = test_client.delete(f"/api/films-views/{randint(1,30)}")
    assert response.status_code == 403

    # admin
    test_client.post(
        "/api/login/",
        json=dict(login=admin.get("email"), password=data_admin["password"]),
    )
    response = test_client.delete(f"/api/films-views/{randint(1,30)}")
    assert response.status_code == 200
