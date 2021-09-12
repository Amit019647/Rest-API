import sqlite3
from models.user import UserModel
from flask_restful import Resource,reqparse
import sqlite3



class UserRegister(Resource):

    parser=reqparse.RequestParser()
    parser.add_argument('username',
    type=str,
    required=True,
    help='This field is necessary.'
    )
    parser.add_argument('password',
    type=str,
    required=True,
    help='This field is necessary.'
    )

    def post(self):
        data=UserRegister.parser.parse_args()

        # if user already exists
        if UserModel.find_by_username(data['username']):
            return {'message':'user already exists'}

        # to insert into the sqlite database rather than the in memory database 
        user=UserModel(**data)
        user.save_to_db()

        return {'message':'User created successfully.'}, 201