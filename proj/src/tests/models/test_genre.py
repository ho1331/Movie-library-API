import pytest
from src.app import app
from src.models.genres import Genre


def test_genre_create():
    with app.app_context():
        genre = Genre.create("23")
        assert genre.get("genre") == "23"
