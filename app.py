from flask import render_template, redirect, url_for, Flask, make_response, jsonify, abort, request
from peewee import *
import uuid
import peewee
from passlib.hash import pbkdf2_sha256
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_bootstrap import Bootstrap

app = Flask(__name__)
sqlite_db = SqliteDatabase('backenddb/backend.sqlite')
app.config.from_object('config')
bootstrap = Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


def generate_password_hash(password):
    return pbkdf2_sha256.encrypt(password, rounds=200000, salt_size=16)


def generate_token():
    return str(uuid.uuid4())


class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=25)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=6, max=20)])
    remember = BooleanField('remember me')


class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=25)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=6, max=20)])


def init_tables():
    with sqlite_db:
        sqlite_db.create_tables([User], safe=True)


def drop_tables():
    sqlite_db.drop_tables([User])


class BaseModel(Model):
    class Meta:
        database = sqlite_db


class User(UserMixin, BaseModel):
    id = IntegerField(primary_key=True)
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()


@login_manager.user_loader
def load_user(user_id):
    return User.get(int(user_id))


@app.route('/')
def index():
    return render_template("index.html",
                           title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            with sqlite_db.atomic():
                user = User.get(User.username == form.username.data)
                if pbkdf2_sha256.verify(form.password.data, user.password):
                    login_user(user, remember=form.remember.data)
                    return redirect(url_for('board'))
                return '<h1> Invalid username or password </h1>'
        except peewee.IntegrityError:
            abort(400)
        except User.DoesNotExist:
            return '<h1> Invalid username or password </h1>'
    return render_template('login.html',
                           form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        try:
            with sqlite_db.atomic():
                new_user = User()
                new_user.username = form.username.data
                new_user.password = generate_password_hash(form.password.data)
                new_user.email = form.email.data
                new_user.save()
                redirect(url_for('board'))
        except peewee.IntegrityError:
            abort(400)
    return render_template('signup.html',
                           form=form)


@app.route('/board')
@login_required
def board():
    return render_template('board.html',
                           title='Board')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(threaded=True, debug=True)
