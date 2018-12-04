correct_username = 'testman'
correct_email = 'testman@outlook.com'
correct_password = 'testman1234'

correct_username2 = 'pupsen'
correct_email2 = 'pupsen@outlook.com'
correct_password2 = 'pupsen1234'

incorrect_username_empty = ''
incorrect_username_short = 'Nas'
incorrect_username_long = 'qwertyuiopasdfghjklzxcvbnm'
incorrect_username_bad_characters = 'a!б.lol'

incorrect_email_no_dog = 'nikita97'
incorrect_email_only_dog = 'nikita97@'
incorrect_email_no_domen = 'nikita97@mail'
incorrect_email_bad_characters = 'nikita_пупкин\/!@outlook.com'

incorrect_password_empty = ''
incorrect_password_short = 'qw2'
incorrect_password_long = 'qwertyuiopasdfghjklzx12345'


# import unittest
#
# from app import app

# class TestCase(unittest.TestCase):
#     def setUp(self):
#         app.config['TESTING'] = True
#         app.config['WTF_CSRF_ENABLED'] = False
#
#     def tearDown(self):
#         pass
#
#     def test_user_incorrect(self):
#         with app.test_client() as client:\
#             res = client.post('/login',
#                           data={'username': incorrect_username2, 'password': correct_password})
#         assert res.status_code == 400

# if __name__ == '__main__':
#     unittest.main()




