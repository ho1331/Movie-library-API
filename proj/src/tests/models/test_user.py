import pytest
from faker import Factory
from src.app import app
from src.models.users import User
from werkzeug.security import check_password_hash

faker = Factory.create()


@pytest.mark.parametrize(
    "user,admin",
    [
        (
            {
                "name": "name1",
                "nick_name": f"nick_name1",
                "email": "name1@gmail.com",
                "password": 12345,
            },
            {
                "name": faker.first_name(),
                "nick_name": f"{faker.last_name_nonbinary()}{faker.suffix()}{faker.prefix()}",
                "email": faker.email(),
                "password": faker.password(),
                "is_admin": True,
            },
        )
    ],
)
def test_user_create(user, admin):
    with app.app_context():
        user1 = User.create(user)
        assert user1.get("name") == "name1"
        assert user1.get("nick_name") == "nick_name1"
        assert user1.get("email") == "name1@gmail.com"
        assert check_password_hash(user1.get("password"), 12345)

        admin1 = User.create(admin)
        assert admin1.get("is_admin") is True
