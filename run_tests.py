from tests.unit_test_signup import SignUpTests
from tests.unit_test_login import LoginTests
from tests.system_test_signup import sysSignUpTest
from tests.system_test_login import sysLoginTest
from tests.integration_tests import DBmanager_test

import unittest
import sys

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    if len(sys.argv) == 1:
        runner.run(unittest.TestSuite((
            unittest.makeSuite(SignUpTests),
            unittest.makeSuite(LoginTests),
            unittest.makeSuite(sysSignUpTest),
            unittest.makeSuite(sysLoginTest),
            unittest.makeSuite(DBmanager_test)
        )))

    elif sys.argv[1] == 'integration':
        runner.run(unittest.makeSuite(DBmanager_test))

    elif sys.argv[1] == 'system':
        runner.run(unittest.TestSuite((
            unittest.makeSuite(sysSignUpTest),
            unittest.makeSuite(sysLoginTest))))

    elif sys.argv[1] == 'unit':
        runner.run(unittest.TestSuite((
            unittest.makeSuite(SignUpTests),
            unittest.makeSuite(LoginTests))))



