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
                                                              200, 201, ""])
            db_manager.login = MagicMock(return_value=[correct_username,
                                                       correct_password,
                                                       200, 200])

            c.post('/signup', data={'username': correct_username,
                                    'email': correct_email,
                                    'password': correct_password})

            res = c.post('/login', data={'username': correct_username, 'password': correct_password})

        assert res.status_code == 200

    def test_login_correct_email(self) :
        with app.test_client() as c:
            db_manager.create_user = MagicMock(return_value=[correct_username,
                                                              correct_email,
                                                              correct_password,
                                                              200, 201, ""])
            db_manager.login = MagicMock(return_value=[correct_email,
                                                       correct_password,
                                                       200, 200])

            c.post('/signup', data={'username': correct_username,
                                    'email': correct_email,
                                    'password': correct_password})

            res = c.post('/login', data={'username': correct_email, 'password': correct_password})

        assert res.status_code == 200


if __name__ == '__main__':
    unittest.main()

