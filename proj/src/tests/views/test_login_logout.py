import pytest
from faker import Factory
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


def test_login_logout(test_client):
    current_user = User.create(authorizate_user)
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
