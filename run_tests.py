from tests.unit_test_signup import SignUpTests
from tests.unit_test_login import LoginTests
from tests.system_test_signup import sysSignUpTest
from tests.system_test_login import sysLoginTest
from tests.integration_tests import DBmanager_test

import unittest
import filecmp


if __name__ == "__main__":
    runner = unittest.TextTestRunner()

    routes_bool = filecmp.cmp('/home/unatart/TodoList/routes/routes.py', '/home/unatart/git/ToDoList/routes/routes.py')
    db_bool = filecmp.cmp('/home/unatart/TodoList/DBmanager/DBmanager.py', '/home/unatart/git/ToDoList/DBmanager/DBmanager.py')

    if routes_bool == False:
        runner.run(unittest.TestSuite((
            unittest.makeSuite(SignUpTests),
            unittest.makeSuite(LoginTests),
            unittest.makeSuite(sysSignUpTest),
            unittest.makeSuite(sysLoginTest)
        )))

    if db_bool == False:
        runner.run(unittest.TestSuite((
            unittest.makeSuite(sysSignUpTest),
            unittest.makeSuite(sysLoginTest),
            unittest.makeSuite(DBmanager_test)
        )))




