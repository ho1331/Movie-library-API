import pytest
from src.tests.mark_parametrize import (
    authorizate_user,
    current_user,
    unauthorizate_user,
)


def test_login_logout(test_client):
    response1 = test_client.post(
        "/api/login/",
        json=dict(
            login=unauthorizate_user["email"], password=unauthorizate_user["password"]
        ),
    )
    response2 = test_client.post(
        "/api/login/",
        json=dict(
            login=current_user.get("email"), password=authorizate_user["password"]
        ),
    )
    response3 = test_client.get("/api/logout/")
    assert response1.status_code == 400
    assert response2.status_code == 200
    assert response3.status_code == 200
