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

VERSION = "1.4"

app = Flask(__name__)

# test Flask server is running
@app.route("/")
def hello():
	return ("Hello from Rock SMS Server v" + VERSION + "!")

@app.route('/sms', methods=['POST'])
def sms():

	# handle request
	app.logger.info(request.form)	
	body = request.form['Body']
	
	# handle response
	response = MessagingResponse()

	#TODO: send error message
	# if response is not good, show details
	#if str(response) != "200 OK":
	#	app.logger.error(str(response))
	#	response.message("Error occurred. The team has been notified!")
	#	return str(response)

	reply = contacts.search(body)
	app.logger.info(reply)	
	response.message(reply)
	return str(response)
	
	#TODO: add a usage help menu and use short codes to choose apps

#TODO: add a feature that reads the staff news when you call in

if __name__ == '__main__':

	#TODO: move this to external class
	# add log file handlers
	fh = logging.RotatingFileHandler("rocksms.log", maxBytes = 10000, backupCount = 1)
	fh.setLevel(logging.INFO)
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	fh.setFormatter(formatter)
	app.logger.addHandler(fh)

	# add email handlers
	#TODO: add email for ERROR messages

	app.run()

