import os

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt import JWT, JWTError

from security import authenticate, identity
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from resources.user import UserRegister

app = Flask(__name__)

app.config['DEBUG'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'secret'
api = Api(app)

jwt = JWT(app, authenticate, identity) # /auth

api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')

@app.errorhandler(JWTError)
def auth_jwt_error(error):
    return jsonify(
        {
            'message': 'Could not validate credentials.',
        }
    ), 401

if __name__ == '__main__':
    from db import db

    db.init_app(app)

    if app.config['DEBUG']:
        with app.app_context():
            db.create_all()

    app.run(port=5000)
