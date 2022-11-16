from src.models.User import User
from src.dao.manager import Manager


class UserManager(Manager):

    @staticmethod
    def add(user: User):
        Manager.create(user=user)

    @staticmethod
    def get_all():
        users = Manager.get_all()
        users = [user_dict(user) for user in users]
        return users

    @staticmethod
    def retrieve():
        """
        It should implemented by child
        :return:
        """
        pass  # pragma: no cover

def user_dict(user):
    return {
        'id': user.id,
        'idz': user.idz,
        'zerynth_api_key': user.zerynth_api_key,
        'email': user.email,
        'name': user.name,
        'surname': user.surname,
        'password': user.password,
        'authenticated': user.authenticated
    }