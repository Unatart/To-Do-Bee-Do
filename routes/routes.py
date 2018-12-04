from flask import render_template, redirect, url_for, request, session, abort
from flask_login import login_required, logout_user, current_user
from flask_api import status
from config import app
from DBmanager.DBmanager import *
import sqlalchemy.exc
from valid_forms.valid_forms import valid_login, valid_signup


# START APP
@app.route('/')
def index():
    if 'id' in session:
        return redirect(url_for('board'))

    return render_template("index.html", title='Home')


# AUTH METHODS
@app.route('/login', methods=['GET', 'POST'])
def login():
    status_code, username, password, form = valid_login()

    if status_code == 200:
        try:
            username, password, id, status_code = db_manager.login(username, password)
            if status_code == 200:
                session['id'] = id
                return redirect(url_for('board')), status.HTTP_200_OK
            elif status_code == 401:
                return render_template('login.html', error='Invalid data, try again or SignUp',
                                       form=form), status.HTTP_401_UNAUTHORIZED

        except sqlalchemy.exc.SQLAlchemyError:
            abort(500)

    return render_template('login.html', form=form), status.HTTP_401_UNAUTHORIZED


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    status_code, username, email, password, form = valid_signup()

    if status_code == 200:
        try:
            username, email, password, id, status_code, error_identity = \
                db_manager.create_user(username, email, password)
            if status_code == 409:
                if error_identity == 'login':
                    return render_template('signup.html', form=form,
                                           error='User with such username exist'), status.HTTP_409_CONFLICT
                if error_identity == 'email':
                    return render_template('signup.html', form=form,
                                           error='User with such email exist'), status.HTTP_409_CONFLICT
            else:
                session['id'] = id
                return redirect(url_for('board')), status.HTTP_200_OK

        except sqlalchemy.exc.SQLAlchemyError:
            return 500

    return render_template('signup.html', form=form), status.HTTP_400_BAD_REQUEST


# FOR TODOLIST
@app.route('/add', methods=['POST'])
def add():
    try:
        if 'id' in session:
            id = session['id']
            user, status_code = db_manager.check_user(id)
            if status_code == 200 and user == current_user:
                todo_text = request.form['todoitem']
                if todo_text is not '':
                    db_manager.create_todo(todo_text, user.id)

    except sqlalchemy.exc.SQLAlchemyError:
        return 500

    return redirect(url_for('board'))


@app.route('/complete/<id>')
def complete(id):
    try:
        if 'id' in session:
            user_id = session['id']
            user, status_code = db_manager.check_user(user_id)
            if status_code == 200 and user == current_user:
                db_manager.complete_todo(id)

    except sqlalchemy.exc.SQLAlchemyError:
        return 500

    return redirect(url_for('board'))


@app.route('/incomplete/<id>')
def incomplete(id):
    try:
        if 'id' in session:
            user_id = session['id']
            user, status_code = db_manager.check_user(user_id)
            if status_code == 200 and user == current_user:
                db_manager.incomplete_todo(id)
    except sqlalchemy.exc.SQLAlchemyError:
        return 500

    return redirect(url_for('board'))


@app.route('/delete/<id>')
def delete(id):
    try:
        if 'id' in session:
            user_id = session['id']
            user, status_code = db_manager.check_user(user_id)
            if status_code == 200 and user == current_user:
                db_manager.delete_todo(id)

    except sqlalchemy.exc.SQLAlchemyError:
        return 500

    return redirect(url_for('board'))


@app.route('/board')
@login_required
def board():
    try:
        if 'id' in session:
            user_id = session['id']
            user, status_code = db_manager.check_user(user_id)
            if status_code == 200 and user == current_user:
                incomplete, complete = db_manager.get_todo(user_id)
        else:
            return redirect(url_for('index'))

    except sqlalchemy.exc.SQLAlchemyError:
        return 500

    return render_template('board.html', incomplete=incomplete, complete=complete, title='Board')


# LOGOUT
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))