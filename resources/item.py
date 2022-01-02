import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from modules.item import ItemModel


class Item(Resource):
    # make sure server receives valid info
    parser = reqparse.RequestParser()
    parser.add_argument('price', 
        type=float, 
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('store_id', 
        type=int, 
        required=True,
        help="Every item needs a store id."
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        else:
            return {"message": "Item not found"}, 404
    

    def post(self, name):
        # if an item with name already there
        if ItemModel.find_by_name(name):
            return {"message": f"An item with name {name} already exists"}, 400
         
        data = Item.parser.parse_args()
        # item = {"name": name, "price": data["price"]}
        item = ItemModel(name, data["price"], data['store_id'])

        # write to db
        try:
            item.save_to_db()
        except:
            # 500 is internal server error
            return {"message": "Error occurred inserting item."}, 500

        return item.json(), 201 # 201 is status code for created
 

    def delete(self, name):
        """connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name, ))
        connection.commit()
        connection.close()

        return {"message": f"Item {name} deleted"} """

        # sql-alchemy easy version
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        
        return {"message": f"Item {name} deleted"}

    def put(self, name):
        data = Item.parser.parse_args()

        # from the db
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, data['price'], data['store_id'])
        else:
            item.price = data['price']

        item.save_to_db()
         
        return item.json()
  

class ItemList(Resource):
    def get(self):
        """connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = "SELECT * FROM items"
        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({"name": row[0], "price": row[1]})

        connection.close()

        return {"items": items}"""
        
        # sql-alchemy easy version
        # ItemModel.query.all() <==> SELECT * FROM items
        return {"items": [item.json() for item in ItemModel.query.all() ] }
