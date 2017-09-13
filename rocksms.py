#! python3
# Copyright 2017 Michael Neeley
# This is the Rock SMS server application

# builtin libs
import os
 
# installed libs
# pip install flask
from flask import Flask, request
# pip install twilio
from twilio.twiml.messaging_response import MessagingResponse
 
# package libs
import contacts

#TODO: look up Redis

app = Flask(__name__)

@app.route('/sms', methods=['POST'])
def sms():
	
	response = MessagingResponse()
	body = request.form['Body']
	response.message(contacts.search(body))
	return str(response)
 
if __name__ == '__main__':
    app.run()

