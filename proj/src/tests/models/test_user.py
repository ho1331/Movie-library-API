import pytest
from faker import Factory
from src.app import app
from src.models.users import User
from werkzeug.security import check_password_hash

faker = Factory.create()

variants = [
    {
        "name": faker.first_name(),
        "nick_name": f"{faker.last_name_nonbinary()}{faker.suffix()}{faker.prefix()}",
        "email": faker.email(),
        "password": faker.password(),
        "is_admin": False,
    },
    {
        "name": faker.first_name(),
        "nick_name": f"{faker.last_name_nonbinary()}{faker.suffix()}{faker.prefix()}",
        "email": faker.email(),
        "password": faker.password(),
        "is_admin": True,
    },
]


@pytest.mark.parametrize("user", variants)
def test_user_create(user):
    with app.app_context():
        user1 = User.create(user)
        assert user1.get("name") == user["name"]
        assert user1.get("nick_name") == user["nick_name"]
        assert user1.get("email") == user["email"]
        assert check_password_hash(user1.get("password"), user["password"])
        assert user1.get("is_admin") is user.get("is_admin")
