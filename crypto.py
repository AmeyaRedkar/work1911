from flask import Flask,request,jsonify
from flask_restful import Resource,Api
from cryptography.fernet import Fernet
from pymongo import MongoClient
from configparser import ConfigParser
import datetime as dt


app=Flask(__name__)
api=Api(app)

config=ConfigParser()
config.read("C:\\Users\\appam\\Desktop\\work1911\\configuration.txt")


mongohost=config.get("db","url")
mongoport=config.get("db","port")
userdb=config.get("db","userdata")
collection=config.get("db","usercollection")

client=MongoClient(mongohost,int(mongoport))

db=client[userdb]
col=db[collection]


key = str(config["genkey"]["key"])

f=Fernet(key)


class Cry(Resource):

	def post(self):
		cryname=(request.json["name"]).encode()
		cryid=(request.json["point"])
		
		col.insert_one({"name":f.encrypt(cryname),"point":cryid})
		return "encrypt is done"
	
	def put(self):
		cryname=(request.json["name"])
		cryid=(request.json["point"])
		bytecry=cryname


		x=list(col.find({"point":cryid}))
		for match in x:
			if bytecry==f.decrypt(match["name"].encode()):
				return "decrypted and matched"


class Waqt(Resource):
	
	def post(self):
		year=request.json["year"]
		month=request.json["month"]		
		day=request.json["day"]		
		minute=request.json["minute"]		
		second=request.json["second"]
		micro=request.json["micro"]


		nowtime=dt.datetime.now()
		custime=dt.datetime(year,month,day,minute,second,micro)
		
		return {
				"Time":str(nowtime),
				"CustomTime":str(custime),
				}

	def put(self):
		cweek=request.json["cweek"]
		cday=request.json["cday"]
		chour=request.json["chour"]
		cminute=request.json["cminute"]
		csecond=request.json["csecond"]

		nowtime=dt.datetime.now()

		comtime=dt.timedelta(weeks=cweek,days=cday,hours=chour,minutes=cminute, seconds=csecond)

		
		return {
		"Time":str(nowtime),
		"afterTime":str(nowtime+comtime)
		} 
		


api.add_resource(Cry,"/")
api.add_resource(Waqt,"/time")


app.run(debug=True)