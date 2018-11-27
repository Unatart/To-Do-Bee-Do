from flask_login import UserMixin
from sqlalchemy import ForeignKey
from config import login_manager
from config import db


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    _username = db.Column('username', db.String(20), unique=True)
    _email = db.Column('email', db.String(35), unique=True)
    password = db.Column(db.String(80))

    todolist = db.relationship('TodoList', backref='user', lazy='dynamic')


class TodoList(db.Model):
    __tablename__ = 'todolist'
    id = db.Column(db.Integer, primary_key=True)
    creator = db.Column(db.String(64), db.ForeignKey('user.username', ondelete='CASCADE'))
    todos = db.relationship('Todo', backref='todolist', lazy='dynamic')


class Todo(db.Model):
    __tablename__ = 'todo'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(128))
    creator = db.Column(db.String(35), db.ForeignKey('user.username', ondelete='CASCADE'))
    complete = db.Column(db.Boolean)
    todolist_id = db.Column(db.Integer, ForeignKey('todolist.id', ondelete='CASCADE'))
