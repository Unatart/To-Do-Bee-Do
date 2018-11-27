from flask import render_template, redirect, url_for, request
from passlib.hash import pbkdf2_sha256
from flask_login import login_user, login_required, logout_user

from forms import LoginForm, RegisterForm
from config import app, db
from models.models import User, Todo
from utils import generate_password_hash


# START APP
@app.route('/')
def index():
    return render_template("index.html",
                           title='Home')


# AUTH METHODS
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(_username=form.username.data).first()
        if user:
                if pbkdf2_sha256.verify(form.password.data, user.password):
                    login_user(user, remember=form.remember.data)
                    return redirect(url_for('board'))
        elif user is None:
            return render_template('login.html', error='Invalid data', form=form)

    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(_username=form.username.data, _email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user, remember=False)
        return redirect(url_for('board'))
    return render_template('signup.html', form=form)


# FOR TODOLIST
@app.route('/add', methods=['POST'])
def add():
    new_todo = Todo()
    new_todo.text = request.form['todoitem']
    new_todo.complete = False
    db.session.add(new_todo)
    db.session.commit()

    return redirect(url_for('board'))


@app.route('/complete/<id>')
def complete(id):
    todo = Todo.query.filter_by(id=int(id)).first()
    todo.complete = True
    db.session.commit()

    return redirect(url_for('board'))


@app.route('/board')
@login_required
def board():
    incomplete = Todo.query.filter_by(complete=False).all()
    complete = Todo.query.filter_by(complete=True).all()
    return render_template('board.html', incomplete=incomplete, complete=complete, title='Board')


# LOGOUT
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))