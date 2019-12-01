from pymongo import MongoClient
from configparser import ConfigParser
from flask_restplus import Resource,reqparse
from flask import Flask,jsonify
from flask_jwt_extended import jwt_required
import os


app=Flask(__name__)


config=ConfigParser()
config.read("C:\\Users\\appam\\Desktop\\work1911\\configuration.txt")


mongohost=config.get("db","url")
mongoport=config.get("db","port")
userdb=config.get("db","shopdata")
collection=config.get("db","shopcollection")

client=MongoClient(mongohost,int(mongoport))

db=client[userdb]
col=db[collection]

itemparser=reqparse.RequestParser()
itemparser.add_argument("item",required=True,help="key as item")
priceparser=reqparse.RequestParser()
priceparser.add_argument("price",required=True,type=float,help="key as price")


class Shopforall(Resource):
	
	def get(self):
		search=list(col.find())
		return str(search)


	
	def post(self):
		item=itemparser.parse_args()
		search=list(col.find({"itemname":item["item"]}))
		return str(search)


class Shopforauth(Resource):

	@jwt_required
	def post(self):
		
		item=itemparser.parse_args()
		pricetag=priceparser.parse_args()

		search=list(col.find({"itemname":item["item"]}))

		for match in search:
			if item["item"]==match["itemname"]:
				return "item {} already exists".format(item["item"])
				
			else:
				col.insert_one({"itemname":item["item"],"price":pricetag["price"]})
				return "new product {} is inserted..!!".format(item["item"])

	@jwt_required	
	def put(self):
		item=itemparser.parse_args()
		pricetag=priceparser.parse_args()
		col.update_one(
			{"itemname":item["item"]},
			{"$set":{"price":pricetag["price"]}})
		return "product {} price is updated".format(item["item"])

	@jwt_required	
	def delete(self):
		item=itemparser.parse_args()
		col.delete_one({"itemname":item["item"]})
		return "product {} is deleted".format(item["item"])