from flask_login import UserMixin
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from . import db
Base = automap_base()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))


'''class User(UserMixin):
    def __init__(self, username, name, password):
        self.name = name
        self.username = username
        self.password = password
    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.name
    def is_active(self):
        """True, as all users are active."""
        return True
    
    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))'''