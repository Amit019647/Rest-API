from flask_restful import Resource,reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

#defining our resource
class Item(Resource):#inheriting the Resource class
    #defing the methods that this resource is going to accept
    # this jwt will first authenticate then go to the get function

    parser =reqparse.RequestParser()
    parser.add_argument('price',
    type=float,
    required=True,
    help="This field cannot be left blank"
    )

    parser.add_argument('store_id',
    type=int,
    required=True,
    help="Every item needs a store id."
    )

    @jwt_required()
    def get(self,name):
        # for in memory database
        '''item =next(filter(lambda x:x['name']==name,items),None)# it just returns the next item filtered else None if no item found next 
        return {'item':item},200 if item is not None else 404#this 404 is is sent to make the status 404 indiacting the error has occured'''
        item=ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message':'Item not found'},404

    def post(self,name):
        # this is used when we use in memory database i.e list
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)},400
            # 400 is for bad request

        data = Item.parser.parse_args()
        #data=request.get_json(silent=True)#this line will give error if the in postman in header key,value is wrong or in body json is not present
        # silent=True ==> it doesn't give error it just returns none
        # force=True ==> it will ensure that we don't need content type header in postman.It will just look into content and just format it
        item=ItemModel(name,**data)
        try:
            item.save_to_db()
        except:
            return {'message':'an error occured while insertion'}, 500#internal server error
        # item.json() ==> this is done because item is an object not a dict so we need to convert it to a json
        return item.json(),201



    def delete(self,name):
        item=ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message':"Item Deleted"}
        return {'message': 'Itemnot found'},404


    def put(self,name):
        data = Item.parser.parse_args()
        #data=request.get_json()
        item = ItemModel.find_by_name(name)

        if item is None:
            item=ItemModel(name,**data)
        else:
            item.price=data['price']

        item.save_to_db()
        return item.json()

class ItemList(Resource):
    def get(self):
        # anyone of below two would work
        # return {'items': [item.json() for item in ItemModel.query.all()]}
        return {'items' : list(map(lambda x:x.json(), ItemModel.query.all()))}


'''from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every item needs a store_id."
                        )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args()

        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': 'Item deleted.'}
        return {'message': 'Item not found.'}, 404

    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item:
            item.price = data['price']
        else:
            item = ItemModel(name, **data)

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}'''