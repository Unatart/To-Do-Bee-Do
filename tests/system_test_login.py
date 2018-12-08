import unittest
from routes.routes import *
from utils import *

class sysLoginTest(unittest.TestCase):
    def setUp(self):
        db.create_all()
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False


    def tearDown(self):
        db.drop_all()


    def test_login_OK_by_username(self):
        with app.test_client() as c:
            c.post('/signup', data={'username': correct_username,
                                          'email': correct_email,
                                          'password': correct_password})
            res = c.post('/login', data={'username': correct_username,
                                         'password': correct_password})

            assert res.status_code == 302


    def test_login_OK_by_email(self):
        with app.test_client() as c:
            c.post('/signup', data={'username': correct_username,
                                          'email': correct_email,
                                          'password': correct_password})
            res = c.post('/login', data={'username': correct_email,
                                         'password': correct_password})

            assert res.status_code == 302


    def test_login_empty_username(self):
        with app.test_client() as c:
            c.post('/signup', data={'username': correct_username,
                                          'email': correct_email,
                                          'password': correct_password})
            res = c.post('/login', data={'username': incorrect_email_empty,
                                         'password': correct_password})

            assert res.status_code == 401


    def test_login_empty_password(self):
        with app.test_client() as c:
            c.post('/signup', data={'username': correct_username,
                                          'email': correct_email,
                                          'password': correct_password})
            res = c.post('/login', data={'username': correct_email,
                                         'password': incorrect_password_empty})

            assert res.status_code == 401


    def test_login_bad_char_username(self):
        with app.test_client() as c:
            c.post('/signup', data={'username': correct_username,
                                          'email': correct_email,
                                          'password': correct_password})
            res = c.post('/login', data={'username': incorrect_username_bad_characters,
                                         'password': correct_password})

            assert res.status_code == 401


    def test_login_short_username(self):
        with app.test_client() as c:
            c.post('/signup', data={'username': correct_username,
                                          'email': correct_email,
                                          'password': correct_password})
            res = c.post('/login', data={'username': incorrect_username_short,
                                         'password': correct_password})

            assert res.status_code == 401


    def test_login_long_username(self):
        with app.test_client() as c:
            c.post('/signup', data={'username': correct_username,
                                          'email': correct_email,
                                          'password': correct_password})
            res = c.post('/login', data={'username': incorrect_username_long,
                                         'password': correct_password})

            assert res.status_code == 401


    def test_login_diff_username(self):
        with app.test_client() as c:
            c.post('/signup', data={'username': correct_username,
                                    'email': correct_email,
                                    'password': correct_password})
            res = c.post('/login', data={'username': correct_username2,
                                         'password': correct_password2})

            assert res.status_code == 401

    def test_login_short_password(self):
        with app.test_client() as c:
            c.post('/signup', data={'username': correct_username,
                                          'email': correct_email,
                                          'password': correct_password})
            res = c.post('/login', data={'username': correct_email,
                                         'password': incorrect_password_short})

            assert res.status_code == 401

    def test_login_long_password(self):
        with app.test_client() as c:
            c.post('/signup', data={'username': correct_username,
                                          'email': correct_email,
                                          'password': correct_password})
            res = c.post('/login', data={'username': correct_email,
                                         'password': incorrect_password_long})

            assert res.status_code == 401




