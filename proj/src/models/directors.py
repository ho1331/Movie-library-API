from sqlalchemy.exc import IntegrityError
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
    def create(dirname: str, sername: str) -> dict:
        """
        create director
        """
        result: dict = {}
        try:
            director = Director(name=dirname, sername=sername)
            result = {
                "name": director.name,
                "sername": director.sername,
            }
            director.save()
        except IntegrityError as exc:
            Director.rollback()
            result = {"Some errors": str(exc)}

        return result
