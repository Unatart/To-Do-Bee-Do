from flask_login import UserMixin
from config import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column('username', db.String(20), unique=True)
    email = db.Column('email', db.String(35), unique=True)
    password = db.Column(db.String(80))
    todos = db.relationship('Todo', backref='creator')


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(128))
    complete = db.Column(db.Boolean)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))


