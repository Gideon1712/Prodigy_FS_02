from . import db
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import date

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')



class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(10))
    first_name = db.Column(db.String(100))
    surname = db.Column(db.String(100))
    dob = db.Column(db.Date)
    address1 = db.Column(db.String(200))
    address2 = db.Column(db.String(200))
    postcode = db.Column(db.String(20))
    county = db.Column(db.String(100))
    country = db.Column(db.String(100))

    user = db.relationship('User', backref=db.backref('profile', uselist=False))


