import unittest
from routes.routes import *
from utils import *

class sysSignUpTest(unittest.TestCase):
    def setUp(self):
        db.create_all()
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False

    def tearDown(self):
        db.drop_all()

    def test_signUp_OK(self):
        with app.test_client() as c:
            res = c.post('/signup', data={'username': correct_username,
                                          'email': correct_email,
                                          'password': correct_password})

            assert res.status_code == 302


    def test_signUp_existing_username(self):
        with app.test_client() as c:
            res = c.post('/signup', data={'username': correct_username,
                                          'email': correct_email,
                                          'password': correct_password})

            assert res.status_code == 302
            res = c.post('/signup', data={'username': correct_username,
                                          'email': correct_email2,
                                          'password': correct_password2})
            assert res.status_code == 409


    def test_signUp_existing_email(self):
        with app.test_client() as c:
            res = c.post('/signup', data={'username': correct_username,
                                          'email': correct_email,
                                          'password': correct_password})

            assert res.status_code == 302
            res = c.post('/signup', data={'username': correct_username2,
                                          'email': correct_email,
                                          'password': correct_password2})
            assert res.status_code == 409


    def test_signUp_empty_username(self):
        with app.test_client() as c:
            res = c.post('/signup', data={'username': incorrect_username_empty,
                                          'email': correct_email,
                                          'password': correct_password})

            assert res.status_code == 409


    def test_signUp_empty_email(self):
        with app.test_client() as c:
            res = c.post('/signup', data={'username': correct_username,
                                          'email': incorrect_email_empty,
                                          'password': correct_password})

            assert res.status_code == 409


    def test_signUp_empty_password(self):
        with app.test_client() as c:
            res = c.post('/signup', data={'username': correct_username,
                                          'email': correct_email,
                                          'password': incorrect_password_empty})

            assert res.status_code == 409


    def test_signUp_nodog_email(self):
        with app.test_client() as c:
            res = c.post('/signup', data={'username': correct_username,
                                          'email': incorrect_email_no_dog,
                                          'password': correct_password})

            assert res.status_code == 409


    def test_signUp_bad_char_email(self):
        with app.test_client() as c:
            res = c.post('/signup', data={'username': correct_username,
                                          'email': incorrect_email_bad_characters,
                                          'password': correct_password})

            assert res.status_code == 409


    def test_signUp_onlydog_email(self):
        with app.test_client() as c:
            res = c.post('/signup', data={'username': correct_username,
                                          'email': incorrect_email_only_dog,
                                          'password': correct_password})

            assert res.status_code == 409


    def test_signUp_short_password(self):
        with app.test_client() as c:
            res = c.post('/signup', data={'username': correct_username,
                                          'email': correct_email,
                                          'password': incorrect_password_short})

            assert res.status_code == 409


    def test_signUp_long_password(self):
        with app.test_client() as c:
            res = c.post('/signup', data={'username': correct_username,
                                          'email': correct_email,
                                          'password': incorrect_password_long})

            assert res.status_code == 409




