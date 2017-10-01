#! python3
# Copyright 2017 Michael Neeley

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

VERSION = "1.3.1"

app = Flask(__name__)

# test Flask server is running
@app.route("/")
def hello():
	return ("Hello from Rock SMS Server v" + VERSION + "!")

@app.route('/sms', methods=['POST'])
def sms():

	#TODO: move this to external class
	# build loggers
	logger = logging.getLogger(__name__)
	logger.setLevel(logging.DEBUG)
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

	# add log file handlers
	fh = logging.FileHandler("rocksms.log")
	fh.setLevel(logging.INFO)
	fh.setFormatter(formatter)
	logger.addHandler(fh)

	# add console handlers
	sh = logging.StreamHandler()
	sh.setLevel(logging.DEBUG)
	sh.setFormatter(formatter)
	logger.addHandler(sh)

	# add email handlers

	# handle request
	logger.info(request.form)	
	body = request.form['Body']
	
	# handle response
	response = MessagingResponse()

	# if response is not good, show details
	#if str(response) != "200 OK":
	#	logger.error(str(response))
	#	response.message("Error occurred. The team has been notified!")
	#	return str(response)

	reply = contacts.search(body)
	logger.info(reply)	
	response.message(reply)
	return str(response)
	
	#TODO: add a usage help menu and use short codes to choose apps

#TODO: add a feature that reads the staff news when you call in

if __name__ == '__main__':
	app.debug = True
	app.run()

