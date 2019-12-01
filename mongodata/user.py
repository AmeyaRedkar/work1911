from pymongo import MongoClient
from configparser import ConfigParser
from flask_restplus import Resource,reqparse
from flask import Flask,redirect,url_for
from flask_jwt_extended import create_access_token
import os 
import datetime
from cryptography.fernet import Fernet



app=Flask(__name__)


config=ConfigParser()
config.read("C:\\Users\\appam\\Desktop\\work1911\\configuration.txt")


mongohost=config.get("db","url")
mongoport=config.get("db","port")
userdb=config.get("db","userdata")
collection=config.get("db","usercollection")

client=MongoClient(mongohost,int(mongoport))

db=client[userdb]
col=db[collection]


userparse=reqparse.RequestParser()
userparse.add_argument('username',required=True,help="key as username")


passwordparse=reqparse.RequestParser()
passwordparse.add_argument('password',required=True,help="key as password")

key = str(config["genkey"]["key"])

f=Fernet(key)


class Signup(Resource):

	def post(self):
		
		user=userparse.parse_args()
		password=passwordparse.parse_args()


		search=list(col.find({"username":user["username"]}))
		

		for match in search :
			if match["username"]==user["username"]:
				return "username {} already exist".format(user['username'])

			

		entry={"username":user["username"],"password":f.encrypt(password["password"].encode())}

		col.insert(entry)

		return "User {} is created".format(user["username"])


class Login(Resource):

	def post(self):
		

		user=userparse.parse_args()
		password=passwordparse.parse_args()

		expire=datetime.timedelta(days=1)

		search=list(col.find({"username":user["username"]}))

		for match in search:
			if match["username"]==user["username"] and f.decrypt(match["password"].encode())==password["password"]:
				access_token=create_access_token(identity=match["username"],expires_delta=expire)
				
				return {
				"access token":access_token
				}

		return "Signup, no username {} exists or incorrect password ".format(user['username'])
				






