"""Ref table by film-genre model"""
from src.app import db
from src.models.base import BaseModel


class Ref(db.Model, BaseModel):
    """
    class condition Film and Genre
    """

    __tablename__ = "ref"
    __table_args__ = (db.PrimaryKeyConstraint("films_id", "genres_id"),)
    films_id = db.Column(
        db.Integer, db.ForeignKey("films.id", ondelete="CASCADE"), nullable=False
    )
    genres_id = db.Column(
        db.Integer, db.ForeignKey("genres.id", ondelete="CASCADE"), nullable=False
    )

    @staticmethod
    def create(data: dict) -> dict:
        """
        create ref
        """
        ref = Ref(**data)
        ref.save()
        result = {
            "films_id": ref.films_id,
            "genres_id": ref.genres_id,
        }

        return result
