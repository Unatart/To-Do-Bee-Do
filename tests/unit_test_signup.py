import unittest
from flask import *
from routes.routes import *
from utils import *
from unittest.mock import MagicMock
from app import app

class SignUpTests(unittest.TestCase):
    def setUp(self):
        self.DBmanager_create_user = db_manager.create_user
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False

    def tearDown(self):
        db_manager.create_user = self.DBmanager_create_user

    def test_signUp_correct(self):
        with app.test_client() as c:
            db_manager.create_user = MagicMock(return_value=[correct_username,
                                                         correct_email,
                                                         correct_password,
                                                         1, 201, ""])
            res = c.post('/signup', data={'username': correct_username,
                                            'email': correct_email,
                                            'password': correct_password})

        assert res.status_code == 302 # FOUND - OK status on redirect

    def test_signUp_existing_username(self):
        with app.test_client() as c:
            db_manager.create_user = MagicMock(return_value=["",
                                                             "",
                                                             "",
                                                             "", 409, "login"])
            res = c.post('/signup', data={'username': correct_username,
                                          'email': correct_email,
                                          'password': correct_password})
        assert res.status_code == 409

    def test_signUp_existing_email(self):
        with app.test_client() as c:
            db_manager.create_user = MagicMock(return_value=["",
                                                             "",
                                                             "",
                                                             "", 409, "email"])
            res = c.post('/signup', data={'username': correct_username,
                                          'email': correct_email,
                                          'password': correct_password})
        assert res.status_code == 409

    def test_signUp_empty_password(self):
        with app.test_client() as c:
            db_manager.create_user = MagicMock(return_value=["",
                                                             "",
                                                             "",
                                                             "", 409, "password"])
            res = c.post('/signup', data={'username': correct_username,
                                          'email': correct_email,
                                          'password': incorrect_password_empty})
        assert res.status_code == 409

    def test_signUp_empty_username(self):
        with app.test_client() as c:
            db_manager.create_user = MagicMock(return_value=["",
                                                             "",
                                                             "",
                                                             "", 409, "login"])
            res = c.post('/signup', data={'username': incorrect_username_empty,
                                          'email': correct_email,
                                          'password': correct_password})
        assert res.status_code == 409

    def test_signUp_empty_email(self):
        with app.test_client() as c:
            db_manager.create_user = MagicMock(return_value=["",
                                                             "",
                                                             "",
                                                             "", 409, "email"])
            res = c.post('/signup', data={'username': correct_username,
                                          'email': incorrect_email_empty,
                                          'password': correct_password})
        assert res.status_code == 409

    def test_signUp_short_username(self):
        with app.test_client() as c:
            db_manager.create_user = MagicMock(return_value=["",
                                                             "",
                                                             "",
                                                             "", 409, "login"])
            res = c.post('/signup', data={'username': incorrect_username_short,
                                          'email': correct_email,
                                          'password': correct_password})
        assert res.status_code == 409

    def test_signUp_long_username(self):
        with app.test_client() as c:
            db_manager.create_user = MagicMock(return_value=["",
                                                             "",
                                                             "",
                                                             "", 409, "login"])
            res = c.post('/signup', data={'username': incorrect_username_long,
                                          'email': correct_email,
                                          'password': correct_password})
        assert res.status_code == 409

    def test_signUp_missing_dog(self):
        with app.test_client() as c:
            db_manager.create_user = MagicMock(return_value=["",
                                                             "",
                                                             "",
                                                             "", 409, "email"])
            res = c.post('/signup', data={'username': correct_username,
                                          'email': incorrect_email_no_dog,
                                          'password': correct_password})
        assert res.status_code == 409

    def test_signUp_incorrect_char(self):
        with app.test_client() as c:
            db_manager.create_user = MagicMock(return_value=["",
                                                             "",
                                                             "",
                                                             "", 409, "email"])
            res = c.post('/signup', data={'username': correct_username,
                                          'email': incorrect_email_bad_characters,
                                          'password': correct_password})
        assert res.status_code == 409





