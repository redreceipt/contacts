#! python3
# Copyright 2017 Michael Neeley
# This is the Rock SMS server application

# builtin libs
import os
import logging
 
# installed libs
# pip install flask
from flask import Flask, request
# pip install twilio
from twilio.twiml.messaging_response import MessagingResponse
 
# package libs
import contacts

app = Flask(__name__)

# test Flask server is running
@app.route("/")
def hello():
	return ("Hello from Rock SMS Server!")

@app.route('/sms', methods=['POST'])
def sms():

	response = MessagingResponse()
	body = request.form['Body']
	response.message(contacts.search(body))
	return str(response)
	
	#TODO: add a usage help menu and use short codes to choose apps

#TODO: add a feature that reads the staff news when you call in

if __name__ == '__main__':
    app.run()

