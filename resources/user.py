import sqlite3
from flask_restful import Resource, reqparse
from modules.user import UserModel
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    jwt_required,
    create_access_token, 
    create_refresh_token, 
    get_jwt_identity
)

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', 
        type=str, 
        required=True,
        help="Username cannot be left blank!"
    )
    parser.add_argument('password', 
        type=str, 
        required=True,
        help="Password cannot be left blank!"
    )
    def post(self):
        data = UserRegister.parser.parse_args()
        # make sure no duplicate users
        if UserModel.find_by_username(data["username"]):
            return {"message": "A user with same username alreayd exists."}, 400

        """connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(query, (data["username"], data["password"]) )

        connection.commit()
        connection.close()"""
        # sql-alchemy easy version
        user = UserModel(**data) # unpack a dictionary
        user.save_to_db()

        return {"message": "User created successfully"}, 201


class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            # user not found:
            return {"message": "User not found"}, 404
        else:
            return user.json()

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            # user not found:
            return {"message": "User not found, unable to delete"}, 404
        else:
            user.delete_from_db()
            return {"message": "User deleted successfully"}, 200


class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', 
        type=str, 
        required=True,
        help="Username cannot be left blank!"
    )
    parser.add_argument('password', 
        type=str, 
        required=True,
        help="Password cannot be left blank!"
    )

    @classmethod
    def post(cls):
        """ 
        get data from parser, 
        find user in db, 
        check password,
        create access token,
        create refresh token,
        Finally return them
        """
        data = cls.parser.parse_args()
        user = UserModel.find_by_username(data['username'])
        
        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id )
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200

        return {"message": "Invalid credentials."}, 401

class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200