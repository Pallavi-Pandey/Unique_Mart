from flask import Flask, request
from flask_restful import Api, Resource, marshal_with, fields
from models import *
from models import db
import os
from datetime import datetime as dt

app = Flask(__name__)
api = (Api(app))



class User_api(Resource):

    def post(self):
        data = request.get_json()
        user = User(id=data.get('id'), name=data.get('name'), email=data.get('email'), 
                    password=data.get('password'), mobile_number=data.get('mobile_number'))
        if User.query.filter_by(id=user.id):
            return "", 404

        db.session.add(user)
        db.session.commit()
        return data, 201