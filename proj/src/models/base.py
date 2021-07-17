"""Model of base class"""
from src.app import db


class BaseModel:
    """
    class of Base model
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
        """
        rollback tranzaction
        """
        db.session.rollback()

    @staticmethod
    def commit():
        """
        commit tranzaction
        """
        db.session.commit()

    @staticmethod
    def get_or_crete(model, **kwargs):
        """
        check query object
        If exist - return object
        Else cretae object
        """
        instance = model.query.filter_by(**kwargs).first()
        if instance:
            return instance
        else:
            instance = model(**kwargs)
            db.session.add(instance)
            db.session.commit()
            return instance

    # @staticmethod
    # def pagination(model, page):
    #     threads = model.query.paginate(per_page=10, page=page, error_out=False)
    #     return threads
