from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db= SQLAlchemy()

class User(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(80), nullable=False)
    surname= db.Column(db.String(80), nullable=False)
    email= db.Column(db.String(80),unique=True, nullable=False)
    password= db.Column(db.Text(),nullable=False)
    created_at = db.Column(db.DateTime, default= datetime.now())

    # string rappresentation of model class
    
    def __repr__(self) ->str:
        return 'User>>> {self.username}'