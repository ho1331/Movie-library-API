"""Director model"""
from src.app import db
from src.models.base import BaseModel


class Director(db.Model, BaseModel):
    """
    class Diretors
    """

    __tablename__ = "directors"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    sername = db.Column(db.String(30), nullable=False)
    films = db.relationship("Film", backref="directors", lazy=True)

    def __init__(self, name: str, sername: str) -> None:
        self.name = name
        self.sername = sername

    @staticmethod
    def create(data: dict) -> dict:
        """
        create director
        """
        result: dict = {}
        director = Director(**data)
        result = {
            "name": director.name,
            "sername": director.sername,
        }
        director.save()
        return result

    @staticmethod
    def delete(id: int):
        """
        delete director by id
        """
        Director.query.filter(Director.id == id).delete()
        Director.commit()
