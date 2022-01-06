import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from flask_jwt_extended import JWTManager

# from security import authenticate, identity
from resources.user import UserRegister, User, UserLogin, TokenRefresh
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

# jwt = JWT(app, authenticate, identity)
jwt = JWTManager(app) # not creating auth

@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    # identity is user.id, see resources/user.py
    if identity == 1:
        return {'is_admin': True}
    else:
        return {'is_admin': False}

# start jwt_extended config
@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        "description": "Token has expired",
        "error": "token_expired"
    }), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        "description": "Token invalid: isn't JWT",
        "error": "invalid_token"
    }), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        "description": "Request missing access_token",
        "error": "token_required"
    }), 401

@jwt.needs_refresh_token_loader
def token_not_fresh_callback():
    return jsonify({
        "description": "Token is not fresh",
        "error": "fresh_token_required"
    }), 401

@jwt.revoked_token_loader
# didn't refresh token but that token should no longer be considered fresh
# e.g. logout within 5 min (before next token refresh takes place)
def revoked_token_callback():
    return jsonify({
        "description": "Token has been revoked",
        "error": "fresh_revoked"
    }), 401


api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>') # since it's a INTEGER primary key
api.add_resource(UserLogin, '/login')
api.add_resource(TokenRefresh, '/refresh')

db.init_app(app)

if __name__ == "__main__":    
    app.run(port=5000, debug=True)
