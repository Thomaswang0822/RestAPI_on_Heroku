import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from db import db
from resources.store import Store, StoreList

app = Flask(__name__)
# Set postgresql as Heroku database. 
env = os.environ.get('DATABASE_URL')
if env:
    # "postgres ..." should become "postgresql ..."
    assert env[:8] == "postgres"
    env = env[:8] + 'ql' + env[8:]
else:
    # keep option of running locally
    env = 'sqlite:///data.db'
app.config['SQLALCHEMY_DATABASE_URI'] = env

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# allow exceptions (by JWT) return their own meaningful error log
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = "ThomasWang"
api = Api(app)


# Let sql-Alchemy create database for us
@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWT(app, authenticate, identity)

api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

db.init_app(app)

if __name__ == "__main__":    
    app.run(port=5000, debug=True)
