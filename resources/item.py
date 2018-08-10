
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser() # erstellt ein Parser Objekt
    parser.add_argument('price',
        type = float,
        required = True,
        help = "This field can not be left blank"
    ) # stellt sicher das ein price argument da ist und dies korrekt ausgefüllt wurde

    parser.add_argument('store_id',
        type = int,
        required = True,
        help = "every item needs a store id"
    ) # stellt sicher das ein price argument da ist und dies korrekt ausgefüllt wurde


    # holt sich ein item aus der Datenbank
    @jwt_required() # sagt das hier ein token erwartet wird
    def get(self,name): #gibt das item aus, wenn es sich in der Liste befindet
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': "item not found"}, 404


    def post(self,name): #haengt ein neues item an die Liste dran
        if ItemModel.find_by_name(name):
            #Item.find_by_name(name): waere auch moeglich
            #next(filter(lambda x: x['name'] == name,items), None): alte if anforderung
            return {'message': "an item with name '{}' already exists".format(name)}, 400

        data = Item.parser.parse_args() # anstelle von request.get_json() data = request.get_json()
        item = ItemModel(name, data['price'], data['store_id']) # item = ItemModel(name, **data)
        try:
            item.save_to_db()
        except:
            return {'message': "an error occured inserting the item."}, 500
        return item.json(), 201 #we always have to return json!!!!!!


    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message': 'Item deleted'}


    #insert or update an item
    def put(self, name):
        data = Item.parser.parse_args() # anstelle von request.get_json()

        item = ItemModel.find_by_name(name)

        if item == None: #wenn item nicht in db, wird es neu angelegt
            item = ItemModel(name, data['price'], data['store_id'])

        else: # item exisitert, wird also nur upgedatet
            item.price = data['price']
            item.store_id = data['store_id']# selbstgeschrieben

        item.save_to_db()

        return item.json()


class ItemList(Resource): # gibt die komplette Liste zurueck
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}
        # mit lambda notation return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}
