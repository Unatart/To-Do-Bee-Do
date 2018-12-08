import unittest
from routes.routes import *
from utils import *

class sysTodoTest(unittest.TestCase):
    def setUp(self):
        db.create_all()
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False

    def tearDown(self):
        db.drop_all()

    def test_add_todo(self):
        with app.test_client() as c:
            c.post('/signup', data={'username': correct_username,
                                          'email': correct_email,
                                          'password': correct_password})
            res = c.post('/login', data={'username': correct_username,
                                         'password': correct_password})

            assert res.status_code == 302

            res = c.post('/add', data={'todoitem': 'hello, world!'})
            assert  res.status_code == 302

    def test_delete_inc_todo(self):
        with app.test_client() as c:
            c.post('/signup', data={'username': correct_username,
                                          'email': correct_email,
                                          'password': correct_password})
            res = c.post('/login', data={'username': correct_username,
                                         'password': correct_password})

            assert res.status_code == 302

            res = c.post('/add', data={'todoitem': 'hello, world!'})
            assert res.status_code == 302

            res = c.get('/delete/1')
            assert res.status_code == 302

    def test_delete_comp_todo(self):
        with app.test_client() as c:
            c.post('/signup', data={'username': correct_username,
                                          'email': correct_email,
                                          'password': correct_password})
            res = c.post('/login', data={'username': correct_username,
                                         'password': correct_password})

            assert res.status_code == 302

            res = c.post('/add', data={'todoitem': 'hello, world!'})
            assert res.status_code == 302

            res = c.get('/complete/1')
            assert res.status_code == 302

            res = c.get('/delete/1')
            assert res.status_code == 302

    def test_complete_todo(self):
        with app.test_client() as c:
            c.post('/signup', data={'username': correct_username,
                                          'email': correct_email,
                                          'password': correct_password})
            res = c.post('/login', data={'username': correct_username,
                                         'password': correct_password})

            assert res.status_code == 302

            res = c.post('/add', data={'todoitem': 'hello, world!'})
            assert res.status_code == 302

            res = c.get('/complete/1')
            assert res.status_code == 302

    def test_incomplete_todo(self):
        with app.test_client() as c:
            c.post('/signup', data={'username': correct_username,
                                          'email': correct_email,
                                          'password': correct_password})
            res = c.post('/login', data={'username': correct_username,
                                         'password': correct_password})

            assert res.status_code == 302

            res = c.post('/add', data={'todoitem': 'hello, world!'})
            assert res.status_code == 302

            res = c.get('/complete/1')
            assert res.status_code == 302

            res = c.get('/incomplete/1')
            assert res.status_code == 302