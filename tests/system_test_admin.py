import unittest
from routes.routes import *
from utils import *

class sysAdminTest(unittest.TestCase):
    def setUp(self):
        db.create_all()
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False

    def tearDown(self):
        db.drop_all()

    def test_login_admin(self):
        with app.test_client() as c:
            c.post('/signup', data={'username': correct_username,
                                    'email': correct_email,
                                    'password': correct_password})
            c.post('/signup', data={'username': correct_username2,
                                    'email': correct_email2,
                                    'password': correct_password2})
            res = c.post('/login', data={'username': 'admin',
                                         'password': 'admin'})
            assert res.status_code == 200

    def test_admin_rights(self):
        with app.test_client() as c:
            c.post('/signup', data={'username': correct_username,
                                    'email': correct_email,
                                    'password': correct_password})
            c.post('/signup', data={'username': correct_username2,
                                    'email': correct_email2,
                                    'password': correct_password2})
            res = c.post('/login', data={'username': 'admin',
                                         'password': 'admin'})
            assert res.status_code == 200
            res = c.get('/admin_board')
            assert res.status_code == 200

    def test_admin_to_board(self):
        with app.test_client() as c:
            res = c.post('/login', data={'username': 'admin',
                                         'password': 'admin'})
            assert res.status_code == 200
            res = c.get('/board')
            assert res.status_code == 401


    def test_admin_delete_user(self):
        with app.test_client() as c:
            c.post('/signup', data={'username': correct_username,
                                    'email': correct_email,
                                    'password': correct_password})
            c.post('/signup', data={'username': correct_username2,
                                    'email': correct_email2,
                                    'password': correct_password2})
            res = c.post('/login', data={'username': 'admin',
                                         'password': 'admin'})
            assert res.status_code == 200
            res = c.get('/admin_board')
            assert res.status_code == 200
            res = c.get('/delete_user/1')
            assert res.status_code == 302

    def test_admin_grant_rights_to_user(self):
        with app.test_client() as c:
            c.post('/signup', data={'username': correct_username,
                                    'email': correct_email,
                                    'password': correct_password})
            c.post('/signup', data={'username': correct_username2,
                                    'email': correct_email2,
                                    'password': correct_password2})
            res = c.post('/login', data={'username': 'admin',
                                         'password': 'admin'})
            assert res.status_code == 200
            res = c.get('/admin_board')
            assert res.status_code == 200
            res = c.get('/grant_rights/1')
            assert res.status_code == 302
            res = c.get('/logout')
            assert res.status_code == 302
            res = c.post('/login', data={'username': correct_username,
                                         'password': correct_password})
            assert res.status_code == 302
            res = c.get('/admin_board')
            assert res.status_code == 200


    def test_admin_delete_rights_to_user(self):
        with app.test_client() as c:
            c.post('/signup', data={'username': correct_username,
                                    'email': correct_email,
                                    'password': correct_password})
            c.post('/signup', data={'username': correct_username2,
                                    'email': correct_email2,
                                    'password': correct_password2})
            res = c.post('/login', data={'username': 'admin',
                                         'password': 'admin'})
            assert res.status_code == 200
            res = c.get('/admin_board')
            assert res.status_code == 200
            res = c.get('/grant_rights/1')
            assert res.status_code == 302
            res = c.get('/delete_rights/1')
            assert res.status_code == 302
            assert res.status_code == 302
            res = c.get('/logout')
            assert res.status_code == 302
            res = c.post('/login', data={'username': correct_username,
                                         'password': correct_password})
            assert res.status_code == 302
            res = c.get('/admin_board')
            assert res.status_code == 401

    def test_user_not_admin(self):
        with app.test_client() as c:
            c.post('/signup', data={'username': correct_username,
                                    'email': correct_email,
                                    'password': correct_password})
            res = c.post('/login', data={'username': correct_username,
                                         'password': correct_password})
            assert res.status_code == 302
            res = c.get('/admin_board')
            assert res.status_code == 401
