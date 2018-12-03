correct_username = 'testman'
correct_email = 'testman@outlook.com'
correct_password = 'testman1234'

correct_username2 = 'pupsen'
correct_email2 = 'pupsen@outlook.com'
correct_password2 = 'pupsen1234'

incorrect_username2 = 'p'
incorrect_email2 = 'pupsen'
incorrect_password2 = 'pup'

import unittest

from app import app

class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False

    def tearDown(self):
        pass

    def test_user_incorrect(self):
        with app.test_client() as client:
            # res = client.get('/login')
            # assert res.status_code == 200
            res = client.post('/login',
                          data={'username': correct_username, 'password': correct_password})
            assert res.status_code == 200

if __name__ == '__main__':
    unittest.main()




