import sqlite3
from db import db

class UserModel(db.Model):
    __tablename__ = 'users' # tells sqlalchemy

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        # self.id = _id
        # id is now auto-incremented by specifying primary_key
        self.username = username
        self.password = password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


    @classmethod
    def find_by_username(cls, username):
        """conn = sqlite3.connect('data.db')
        cursor = conn.cursor()

        query = "SELECT * FROM users WHERE username=?"
        # parameter, even only 1, should be in tuple
        result = cursor.execute(query, (username,) )
        print(type(result))
        row = result.fetchone() # returns None if nothing in result
        if row:
            user = cls(*row)
        else:
            user = None
        conn.close()
        return user"""

        # sql-alchemy easy version
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        """conn = sqlite3.connect('data.db')
        cursor = conn.cursor()

        query = "SELECT * FROM users WHERE id=?"
        # parameter, even only 1, should be in tuple
        result = cursor.execute(query, (_id,) )
        print(type(result))
        row = result.fetchone() # returns None if nothing in result
        if row:
            user = cls(*row)
        else:
            user = None
        conn.close()
        return user"""

        # sql-alchemy easy version
        return cls.query.filter_by(id=_id).first()