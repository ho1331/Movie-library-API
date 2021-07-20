"""Create test-Api client for all tests"""

import pytest
from src.main import api


@pytest.fixture(scope="module")
def test_client():
    # Create a test client using the Flask application configured for testing
    with api.app.test_client() as testing_client:
        # Establish an application context
        with api.app.app_context():
            yield testing_client
