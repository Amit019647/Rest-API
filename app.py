import os

from security import identity
from flask import Flask,request
from flask.json import jsonify
from flask_restful import Resource,Api,reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate,identity
from resources.user import UserRegister
from resources.item import Item,ItemList
from resources.store import StoreList,Store

#having the api
app=Flask(__name__)#creates our app
app.config['SQLALCHEMY_DATABASE_URI']=os.environ.get('DATABASE_URL','sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.secret_key = 'jose'
api=Api(app)

jwt=JWT(app,authenticate,identity)#in this jwt uses app,authenticate,identity together to allow authentication of users
# it will create an new end point /auth

#added the resource here
api.add_resource(Store,'/store/<string:name>')
api.add_resource(Item,'/item/<string:name>') #http;//127.0.0.1:5000/student/Name
api.add_resource(ItemList,'/items')
api.add_resource(StoreList,'/stores')

api.add_resource(UserRegister,'/register')

if __name__=="__main__":
    from db import db
    db.init_app(app)
    app.run(port=5000,debug=True)

