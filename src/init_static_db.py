from src.dao.UserManager import UserManager
from src.models.User import User


# create default user
def init_user():
    user = User(
        email="gustavo.milan@email.com",
        name="Gustavo",
        surname="Milan",
        password="gustavo1",
        apikey_zerynth="G9froN8D4R.cF1znVzGvCejjc5BrzCsSqcqMaANPgRmFXMglCAWhkYttQFTymThnrf1ta7OQVP4",
        id_zerynth="acc-6sdna7wlhpno",
    )  
    UserManager.register(user)