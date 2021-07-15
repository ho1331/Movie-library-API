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

    @staticmethod
    def get_or_crete(model, **kwargs):
        instance = model.query.filter_by(**kwargs).first()
        if instance:
            return instance
        else:
            instance = model(**kwargs)
            db.session.add(instance)
            db.session.commit()
            return instance

