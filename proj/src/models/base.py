from src.app import db


class BaseModel:
    """
    class of Base model views
    """

    def save(self):
        """
        commit tranzaction
        """
        db.session.add(self)
        db.session.commit()
        return self

    @staticmethod
    def rollback():
        db.session.rollback()

    @staticmethod
    def commit():
        db.session.commit()
