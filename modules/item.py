# import sqlite3
from db import db

"""
update and insert have been changed from classmethod to instance method
find_by_name stays the same
"""
class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    # info for store.py
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id
    
    def json(self):
        return {'name': self.name, 'price': self.price}


    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
    
    def insert(self):
        """# write to db
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (self.name, self.price))
        connection.commit()
        connection.close()"""

        # sql-alchemy easy version
        db.session.add(self)
        db.session.commit()

    # a proper name after the change
    def save_to_db(self):
        # sql-alchemy easy version
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls, name):
        """connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name, ))
        row = result.fetchone()
        connection.close()

        if row:
            return cls(*row)
        return None"""
        # sql-alchemy easy version

        # similar to "SELECT * FROM items WHERE name=name LIMIT 1"
        return ItemModel.query.filter_by(name=name).first()
    
