import unittest
from routes.routes import *
from utils import *


class DBmanager_test(unittest.TestCase):
    def setUp(self):
        db.create_all()
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False

    def tearDown(self):
        db.drop_all()

    def test_signUp_OK(self):
        u, e, p, id, status_code, error = db_manager.create_user(correct_username, correct_email, correct_password)
        db_user = User.query.filter_by(username=correct_username).first()

        assert db_user.username == correct_username
        assert status_code == 201
        assert error == ""


    def test_signUp_UserExist_by_username(self):
        db_manager.create_user(correct_username, correct_email, correct_password)
        db_user = User.query.filter_by(username=correct_username).first()
        assert db_user.username == correct_username

        u, e, p, id, status_code, error = db_manager.create_user(correct_username, correct_email2, correct_password2)
        assert status_code == 409
        assert error == 'login'


    def test_signUp_UserExist_by_email(self):
        db_manager.create_user(correct_username, correct_email, correct_password)
        db_user = User.query.filter_by(username=correct_username).first()
        assert db_user.username == correct_username

        u, e, p, id, status_code, error = db_manager.create_user(correct_username2, correct_email, correct_password2)
        assert status_code == 409
        assert error == 'email'

    def test_login_OK_by_username(self):
        db_manager.create_user(correct_username, correct_email, correct_password)

        login, p, id, status_code = db_manager.login(correct_username, correct_password)

        assert login == correct_username
        assert status_code == 200


    def test_login_OK_by_email(self):
        db_manager.create_user(correct_username, correct_email, correct_password)

        login, p, id, status_code = db_manager.login(correct_email, correct_password)

        assert login == correct_email
        assert status_code == 200

    def test_login_incorrect_password(self):
        db_manager.create_user(correct_username, correct_email, correct_password)

        l, password, id, status_code = db_manager.login(correct_email, incorrect_password_long)

        assert status_code == 401
        assert l == ""
        assert password == ""
        assert id == ""
