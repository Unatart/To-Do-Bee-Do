from models.models import User, Todo
from config import db
from passlib.hash import pbkdf2_sha256
from flask_login import login_user
from validator.validator import Validator


def generate_password_hash(password):
    return pbkdf2_sha256.encrypt(password, rounds=200000, salt_size=16)


class DBmanager:
    # 409 - Conflict, 201 - Created
    def create_user(self, init_login, init_email, init_password):
        if Validator.validate_password(init_password) == True :

            if Validator.validate_username(init_login) == False:
                return "", "", "", "", 409, "login"
            if User.query.filter_by(username=init_login).first():
                return "", "", "", "", 409, "login"

            if Validator.validate_email(init_email) == False:
                return "", "", "", "", 409, "email"
            if User.query.filter_by(email=init_email).first():
                return "", "", "", "", 409, "email"

            hashed_password = generate_password_hash(init_password)
            new_user = User(username=init_login,
                            email=init_email,
                            password=hashed_password)
            db.session.add(new_user)
            db.session.commit()

        else:
            return "", "", "", "", 409, "password"


        return new_user.username, new_user.email, new_user.password, new_user.id, 201, ""


    # 401, 200
    def login(self, init_login, init_password):
        user = User.query.filter_by(username=init_login).first()
        if user and pbkdf2_sha256.verify(init_password, user.password):
            return user.username, user.password, user.id, 200

        user = User.query.filter_by(email=init_login).first()
        if user and pbkdf2_sha256.verify(init_password, user.password):
            return user.email, user.password, user.id, 200

        return "", "", "", 401

    def check_user(self, init_id):
        user = User.query.filter_by(id=init_id).first()
        if user:
            return user, 200

        return "", 403


    def create_todo(self, init_text, user_id):
        new_todo = Todo(text=init_text, complete=False, creator_id=user_id)
        db.session.add(new_todo)
        db.session.commit()


    def incomplete_todo(self, init_id):
        todo = Todo.query.filter_by(id=int(init_id)).first()
        todo.complete = False
        db.session.commit()


    def complete_todo(self, init_id):
        todo = Todo.query.filter_by(id=int(init_id)).first()
        todo.complete = True
        db.session.commit()


    def delete_todo(self, init_id):
        Todo.query.filter_by(id=init_id).delete()
        db.session.commit()

    def get_todo(self, init_user_id):
        incomplete = Todo.query.filter_by(creator_id=init_user_id, complete=False).all()
        complete = Todo.query.filter_by(creator_id=init_user_id, complete=True).all()

        return incomplete, complete


db_manager = DBmanager()

