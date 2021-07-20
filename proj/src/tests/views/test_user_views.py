import pytest
from src.tests.mark_parametrize import data_test_film_crete, data_to_test_user_create


def test_user_list__get(test_client):
    response = test_client.get("/api/users/")
    assert response.status_code == 200


@pytest.mark.parametrize("user", data_to_test_user_create)
def test_user_post(test_client, user):
    response = test_client.post("/api/users/", json=user)
    assert response.status_code == 201

    response = test_client.post("/api/users/", json=data_test_film_crete[0][0])
    assert response.status_code == 400
