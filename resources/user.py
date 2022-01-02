import sqlite3
from flask_restful import Resource, reqparse
from modules.user import UserModel

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