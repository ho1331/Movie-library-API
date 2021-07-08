from sqlalchemy.exc import IntegrityError
from src.app import db
from src.models.base import BaseModel


class Genre(db.Model, BaseModel):
    """
    class Genre
    """

    __tablename__ = "genres"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    genre = db.Column(db.String(30), unique=True, nullable=False)
    # filmses = db.relationship("Film", secondary="ref", backref="genres", lazy=True)

    def __init__(self, genre: str) -> None:
        self.genre = genre

    @staticmethod
    def create(genre: str) -> dict:
        """
        create genre
        """
        result: dict = {}
        try:
            genres = Genre(genre=genre)
            result = {"genre": genres.genre}
            genres.save()
        except IntegrityError as exc:
            Genre.rollback()
            result = {"Some errors": str(exc)}

        return result
