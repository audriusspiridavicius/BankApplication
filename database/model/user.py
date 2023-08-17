from flask_login import UserMixin

from init import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    picture = db.Column(db.String(300), nullable=False, default='default.png')