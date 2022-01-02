# Copied from modules/item.py
from db import db

class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    # sql_Alchemy will go to item.py and see store_id
    # and this is a list of different items in this store
    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, name):
        self.name = name
    
    def json(self):
        # Because of lazy='dynamic', self.items is now a query, not an actual list
        return {'name': self.name, 'items': [item.json() for item in self.items.all()]}

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
    
    def insert(self):
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
        # similar to "SELECT * FROM items WHERE name=name LIMIT 1"
        return StoreModel.query.filter_by(name=name).first()
    
