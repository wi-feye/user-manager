from src import db
from src.models.User import User


class Manager(object):

    db_session = db.session

    @staticmethod
    def check_none(**kwargs):
        for name, arg in zip(kwargs.keys(), kwargs.values()):
            if arg is None:
                raise ValueError("You can't set %s argument to None" % name)

    @staticmethod
    def create(**kwargs):
        Manager.check_none(**kwargs)
        for bean in kwargs.values():
            db.session.add(bean)

        db.session.commit()

    @staticmethod
    def get_all():
        return db.session.query(User).all()

    @staticmethod
    def update(**kwargs):
        Manager.check_none(**kwargs)
        db.session.commit()

    @staticmethod
    def delete(**kwargs):
        Manager.check_none(**kwargs)

        for bean in kwargs.values():
            db.session.delete(bean)
        db.session.commit()

    @staticmethod
    def get_user_by_email(email):
        return db.session.query(User).filter_by(email=email).first()

    @staticmethod
    def get_user_by_id(id):
        return db.session.query(User).filter_by(id=id).first()

    @staticmethod
    def get_user_by_idz(idz):
        return db.session.query(User).filter_by(idz=idz).first()      

    @staticmethod
    def get_user_by_idz(idz):
        return db.session.query(User).filter_by(idz=idz).first()      

    @staticmethod
    def get_user_by_zerynth_api_key(zerynth_api_key):
        return db.session.query(User).filter_by(zerynth_api_key=zerynth_api_key).first()         


        
