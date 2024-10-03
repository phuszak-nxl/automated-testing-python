from models.item import ItemModel
from models.store import StoreModel
from models.user import UserModel
from tests.base_test import BaseTest
import json


class ItemTest(BaseTest):
    def setUp(self):
        super(ItemTest, self).setUp()
        with self.app() as client:
            with self.app_context():
                UserModel('test_user', '1234').save_to_db()
                auth_req = client.post('/auth', data=json.dumps({
                    'username': 'test_user',
                    'password': '1234'
                }), headers={'Content-Type': 'application/json'})
                self.auth_header = "JWT {}".format(json.loads(auth_req.data)['access_token'])

    def test_get_item_no_auth(self):
        with self.app() as client:
            resp = client.get('/item/test_item')
            self.assertEqual(resp.status_code, 401)

    def test_item_not_found(self):
        with self.app() as client:
            resp = client.get('/item/test', headers={'Authorization': self.auth_header})
            self.assertEqual(resp.status_code, 404)

    def test_get_item(self):
        with self.app() as client:
            with self.app_context():
                ItemModel('test_item', 19.99, 1).save_to_db()
                resp = client.get('/item/test_item', headers={'Authorization': self.auth_header})
                self.assertEqual(resp.status_code, 200)

    def test_create_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                resp = client.post('/item/test', json={'price': 19.99, 'store_id': 1})
                self.assertEqual(resp.status_code, 201)
                self.assertDictEqual({'name': 'test', 'price': 19.99}, json.loads(resp.data))

    def test_create_duplicate_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 19.99, 1).save_to_db()
                resp = client.post('/item/test', json={'price': 19.99, 'store_id': 1})
                self.assertEqual(resp.status_code, 400)
                self.assertDictEqual({'message': "An item with name 'test' already exists."}, json.loads(resp.data))

    def test_put_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                resp = client.put('/item/test', json={'price': 19.99, 'store_id': 1})
                self.assertEqual(resp.status_code, 200)
                self.assertEqual(ItemModel.find_by_name('test').price, 19.99)
                self.assertDictEqual({'name': 'test', 'price': 19.99}, json.loads(resp.data))

    def test_put_update_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 5.99, 1).save_to_db()
                self.assertEqual(ItemModel.find_by_name('test').price, 5.99)
                resp = client.put('/item/test', json={'price': 19.99, 'store_id': 1})
                self.assertEqual(resp.status_code, 200)
                self.assertEqual(ItemModel.find_by_name('test').price, 19.99)
                self.assertDictEqual({'name': 'test', 'price': 19.99}, json.loads(resp.data))

    def test_delete_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test_item', 19.99, 1).save_to_db()
                resp = client.delete('/item/test_item')
                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual({
                    'message': 'Item deleted'
                }, json.loads(resp.data))

    def test_item_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 5.99, 1).save_to_db()
                resp = client.get('/items')
                self.assertDictEqual({
                    'items': [
                        {
                            'name': 'test', 'price': 5.99
                        }
                    ]
                }, json.loads(resp.data))