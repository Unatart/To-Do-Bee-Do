import unittest
from flask import *
from routes.routes import *
from utils import *
from unittest.mock import MagicMock
from app import app


class LoginTests(unittest.TestCase):
    def setUp(self):
        self.DBmanager_create_user = db_manager.create_user
        self.DBmanager_login = db_manager.login
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False

    def tearDown(self):
        db_manager.create_user = self.DBmanager_create_user
        db_manager.login = self.DBmanager_login

    def test_login_correct_username(self) :
        with app.test_client() as c:
            db_manager.create_user = MagicMock(return_value=[correct_username,
                                                              correct_email,
                                                              correct_password,
                                                              1, 201, ""])
            db_manager.login = MagicMock(return_value=[correct_username,
                                                       correct_password,
                                                       1, 200])

            c.post('/signup', data={'username': correct_username,
                                    'email': correct_email,
                                    'password': correct_password})

            res = c.post('/login', data={'username': correct_username, 'password': correct_password})

        assert res.status_code == 302  # FOUND

    def test_login_correct_email(self) :
        with app.test_client() as c:
            # username, email, password, id, status_code, identity for error
            db_manager.create_user = MagicMock(return_value=[correct_username,
                                                              correct_email,
                                                              correct_password,
                                                              1, 201, ""])
            db_manager.login = MagicMock(return_value=[correct_email,
                                                       correct_password,
                                                       1, 200])

            c.post('/signup', data={'username': correct_username,
                                    'email': correct_email,
                                    'password': correct_password})

            res = c.post('/login', data={'username': correct_email, 'password': correct_password})

        assert res.status_code == 302 # FOUND

    def test_login_not_user_by_username(self):
        with app.test_client() as c:
            db_manager.create_user = MagicMock(return_value=[correct_username,
                                                             correct_email,
                                                             correct_password,
                                                             1, 201, ""])
            db_manager.login = MagicMock(return_value=["", "", "", 401])

            c.post('/signup', data={ 'username': correct_username,
                                     'email': correct_email,
                                     'password': correct_password })
            res = c.post('/login', data={'username': correct_username2, 'password': correct_password})

        assert res.status_code == 401

    def test_login_not_user_by_email(self):
        with app.test_client() as c:
            db_manager.create_user = MagicMock(return_value=[correct_username,
                                                             correct_email,
                                                             correct_password,
                                                             1, 201, ""])
            db_manager.login = MagicMock(return_value=["", "", "", 401])

            c.post('/signup', data={'username': correct_email,
                                    'email': correct_email,
                                    'password': correct_password})
            res = c.post('/login', data={'username': correct_email2, 'password': correct_password})

        assert res.status_code == 401

    def test_login_not_user_by_password(self):
        with app.test_client() as c:
            db_manager.create_user = MagicMock(return_value=[correct_username,
                                                             correct_email,
                                                             correct_password,
                                                             1, 201, ""])
            db_manager.login = MagicMock(return_value=["", "", "", 401])

            c.post('/signup', data={'username': correct_email,
                                    'email': correct_email,
                                    'password': correct_password})
            res = c.post('/login', data={'username': correct_email, 'password': correct_password2})

        assert res.status_code == 401

    def test_login_empty_username(self):
        with app.test_client() as c:
            db_manager.create_user = MagicMock(return_value=[correct_username,
                                                             correct_email,
                                                             correct_password,
                                                             1, 201, ""])
            db_manager.login = MagicMock(return_value=["", "", "", 401])
            c.post('/signup', data={'username': correct_email,
                                    'email': correct_email,
                                    'password': correct_password})
            res = c.post('/login', data={'username': incorrect_username_empty, 'password': correct_password})

        assert res.status_code == 401

    def test_login_empty_password(self):
        with app.test_client() as c:
            db_manager.create_user = MagicMock(return_value=[correct_username,
                                                             correct_email,
                                                             correct_password,
                                                             1, 201, ""])
            db_manager.login = MagicMock(return_value=["", "", "", 401])
            c.post('/signup', data={'username': correct_email,
                                    'email': correct_email,
                                    'password': correct_password})
            res = c.post('/login', data={'username': correct_username, 'password': incorrect_password_empty})

        assert res.status_code == 401


