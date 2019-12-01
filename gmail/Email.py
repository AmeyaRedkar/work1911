from flask import Flask
from flask_restplus import Resource,Api,reqparse
from flask_mail import Message, Mail
from configparser import ConfigParser



mail=Mail()
app=Flask(__name__)
mail.init_app(app)
api=Api(app)
config=ConfigParser()
config.read("C:\\Users\\appam\\Desktop\\work1911\\configuration.txt")


app.config["MAIL_SERVER"]="smtp.gmail.com"
app.config["MAIL_PORT"]=587
app.config["MAIL_USERNAME"]=config.get("flaskmail","usermail")
app.config["MAIL_PASSWORD"]=config.get("flaskmail","password")
app.config["MAIL_USE_TLS"]=True
app.config["MAIL_USE_SSL"]=False


subparse=reqparse.RequestParser()
subparse.add_argument('subject',required=True,help="key as subject")
senderparse=reqparse.RequestParser()
senderparse.add_argument('sender',required=True,help="key as sender")
recipientparse=reqparse.RequestParser()
recipientparse.add_argument('recipient',action="append",required=True,help="key as recipients")
bodyparse=reqparse.RequestParser()
bodyparse.add_argument('body',required=True,help="key as body")

class GMail(Resource):
	
	def post(self):
		sub=subparse.parse_args()
		sendermail=senderparse.parse_args()
		recipientmail=recipientparse.parse_args()
		bodymessage=bodyparse.parse_args()

	

		msg=Message()
		msg.subject=sub["subject"]
		msg.sender=sendermail["sender"]
		msg.recipients=recipientmail["recipient"]
		msg.body=bodymessage["body"]
		mail.send(msg)

		return "message is send"




