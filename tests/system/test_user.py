from models.user import UserModel
from tests.base_test import BaseTest
import json


class UserTest(BaseTest):
    def test_register_user(self):
        with self.app() as client:
            with self.app_context():
                req = client.post('/register', json={'username': 'test', 'password': '1234'})
                self.assertEqual(req.status_code, 201)
                self.assertIsNotNone(UserModel.find_by_username('test'))
                self.assertDictEqual({'message': 'User created successfully.'}, json.loads(req.data))

    def test_login_user(self):
        with self.app() as client:
            with self.app_context():
                client.post('/register', json={'username': 'test', 'password': '1234'})
                auth_req = client.post('/auth',
                                       data=json.dumps({'username': 'test', 'password': '1234'}),
                                       headers={'Content-Type': 'application/json'})
                self.assertIn('access_token', json.loads(auth_req.data).keys())

    def test_register_duplicate_user(self):
        with self.app() as client:
            with self.app_context():
                client.post('/register', json={'username': 'test', 'password': '1234'})
                resp = client.post('/register', json={'username': 'test', 'password': '1234'})
                self.assertEqual(resp.status_code, 400)
                self.assertDictEqual({'message': 'Username already registered.'}, json.loads(resp.data))