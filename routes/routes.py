from flask import render_template, redirect, url_for, request, session, abort
from flask_api import status
from config import app
from DBmanager.DBmanager import *
import sqlalchemy.exc
from get_forms.get_forms import get_login, get_signup


# START APP
@app.route('/')
def index():
    return render_template("index.html", title='Home')


# AUTH METHODS
@app.route('/login', methods=['GET', 'POST'])
def login():
    status_code, username, password, form = get_login()

    if username == 'admin' and password == 'admin':
        users = db_manager.get_all_users()
        session['id'] = 777
        return render_template('admin_board.html', users = users)

    if status_code == 200:
        try:
            username, password, id, status_code = db_manager.login(username, password)
            if status_code == 200:
                session['id'] = id
                return redirect(url_for('board'))
            elif status_code == 401:
                return render_template('login.html', error='Invalid data, try again or SignUp',
                                       form=form), status.HTTP_401_UNAUTHORIZED

        except sqlalchemy.exc.SQLAlchemyError:
            abort(500)

    return render_template('login.html', form=form), status.HTTP_200_OK


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    status_code, username, email, password, form = get_signup()

    if status_code == 200:
            username, email, password, id, status_code, error_identity = \
                db_manager.create_user(username, email, password)
            if status_code == 409:
                if error_identity == 'login':
                    return render_template('signup.html', form=form,
                                           error='Incorrect username'), status.HTTP_409_CONFLICT
                if error_identity == 'email':
                    return render_template('signup.html', form=form,
                                           error='Incorrect email'), status.HTTP_409_CONFLICT
                if error_identity == 'password':
                    return render_template('signup.html', form=form,
                                           error='Incorrect password'), status.HTTP_409_CONFLICT
            else:
                session['id'] = id
                return redirect(url_for('board'))

    return render_template('signup.html', form=form), status.HTTP_200_OK


# FOR TODOLIST
@app.route('/add', methods=['POST'])
def add():
    try:
        if 'id' in session:
            id = session['id']
            user, status_code = db_manager.check_user(id)
            if status_code == 200:
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
            if status_code == 200:
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
            if status_code == 200:
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
            if status_code == 200:
                db_manager.delete_todo(id)

    except sqlalchemy.exc.SQLAlchemyError:
        return 500

    return redirect(url_for('board'))


@app.route('/delete_user/<id>')
def delete_user(id):
    db_manager.delete_user(id)
    return redirect(url_for('admin_board'))


@app.route('/grant_rights/<id>')
def grant_rights(id):
    db_manager.grant_rights(id)
    return redirect(url_for('admin_board'))


@app.route('/delete_rights/<id>')
def delete_rights(id):
    db_manager.delete_rights(id)
    return redirect(url_for('admin_board'))


@app.route('/board')
def board():
    incomplete = ""
    complete = ""
    access = False
    if 'id' in session:
        user_id = session['id']
        user, status_code = db_manager.check_user(user_id)
        if status_code == 200:
            incomplete, complete = db_manager.get_todo(user_id)
            access = db_manager.check_rights(user_id)
    else:
        return redirect(url_for('index'))

    return render_template('board.html', incomplete=incomplete, complete=complete, access=access, title='Board')


@app.route('/admin_board')
def admin_board():
    if 'id' in session:
        user_id = session['id']
        if user_id == 777:
            users = db_manager.get_all_users()
            return render_template('admin_board.html', users=users)
        user, status_code = db_manager.check_user(user_id)
        if status_code == 200:
            access = db_manager.check_rights(user_id)
            if access == True:
                users = db_manager.get_all_users()
                return render_template('admin_board.html', users = users)

    return redirect(url_for('board')), status.HTTP_401_UNAUTHORIZED


# LOGOUT
@app.route('/logout')
def logout():
    return redirect(url_for('index'))