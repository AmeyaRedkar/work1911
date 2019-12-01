from flask import Flask
from flask_restplus import Resource, Api
from flask_jwt_extended import JWTManager
from configparser import ConfigParser
from mongodata.user import Login,Signup
from mongodata.shop import Shopforall,Shopforauth
from gmail.Email import GMail
import os

config=ConfigParser()
config.read("C:\\Users\\appam\\Desktop\\work1911\\configuration.txt")


app=Flask(__name__)

api=Api(app)

app.secret_key=config.get('flask','secret_key')

jwtmanager=JWTManager(app)



api.add_resource(Login,"/login")
api.add_resource(Signup,"/signup")
api.add_resource(Shopforauth,"/membershop")
api.add_resource(Shopforall,"/shop")
#api.add_resource(GMail,"/mail")


app.run(port=5000,debug=True)

