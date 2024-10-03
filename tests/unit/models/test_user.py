from models.user import UserModel
from tests.base_test import BaseTest

class UserTest(BaseTest):
    def test_create_user(self):
        user = UserModel('test', 'abcd')
        self.assertEqual(user.username, 'test', 'Could not create user with the given username.')
        self.assertEqual(user.password, 'abcd', 'Could not create user with the given password.')