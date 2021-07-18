import pytest
from src.app import create_app


@pytest.fixture(scope="module")
def test_client():
    flask_app = create_app()

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client  # this is where the testing happens!


def test_login_logout(test_client):
    response = test_client.post(
        "/login/", data=dict(login="3", password="3"), follow_redirects=True
    )
    assert response.status_code == 404

    response = test_client.get("/login/")
    assert response.status_code == 404
