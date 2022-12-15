from src import db

# default library salt length is 8
# adjusting it to 16 allow us to improve the strongness of the password
_SALT_LENGTH = 16


class User(db.Model):
    """Representation of User model."""

    # The name of the table that we explicitly set
    __tablename__ = 'User'

    # A list of fields to be serialized
    SERIALIZE_LIST = ['id', 'id_zerynth', 'apikey_zerynth' 'email', 'name', 'surname', 'password', 'telegram_username']

    # All fields of user
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_zerynth = db.Column(db.String(20), unique=True,nullable=False)
    apikey_zerynth = db.Column(db.String(), unique=True)
    email = db.Column(db.Unicode(128), unique=True, nullable=False)
    name = db.Column(db.Unicode(128), nullable=False)
    surname = db.Column(db.Unicode(128), nullable=False)
    password = db.Column(db.Unicode(128), nullable=False)
    telegram_username = db.Column(db.String(32), nullable=True)

    def __init__(self, *args, **kw):
        super(User, self).__init__(*args, **kw)
        self.authenticated = False

    def serialize(self):
        return dict([(k, self.__getattribute__(k)) for k in self.SERIALIZE_LIST])