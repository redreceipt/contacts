#! python3
# Copyright 2017 Michael Neeley
#
# This contains the main functions

# built-in libs
import os, pdb
from os.path import join, dirname

# installed libs
from robobrowser import RoboBrowser # pip install robobrowser
from twilio.rest import Client # pip install twilio
from twilio.base.exceptions import TwilioRestException
from dotenv import load_dotenv # pip install -U python-dotenv

###from base64 import b64decode, b64encode
import pdb

def getContact(to = "", contact = "", send = False):
	"""
	Will get the contact info and send back to user.
	
	PARAMS:
		(str) to - phone number to send info
		(str) contact - person to search for
		(bool) send - flag to send text *WILL COST $$$*
	RETURNS:
		0 - Success.
	"""

	sms = find(contact, session)
	if send: _testSend(to, sms, env)

	return 0

def _login(user = "", pw = "", v = False):
	"""
	Will login using given credentials to Rock.
	"""

	loginPage = ("https://rock.newspring.cc")

	# testing robobrowser
	browser = RoboBrowser(history = True, parser = "lxml")
	browser.open(loginPage)
	form = browser.get_forms()[0]
	form["ctl17$ctl01$ctl00$tbUserName"].value = user
	form["ctl17$ctl01$ctl00$tbPassword"].value = pw
	submitBtn = "ctl17$ctl01$ctl00$btnLogin"
	browser.submit_form(form, submit = form[submitBtn])
	if v: print("Response URL: " + browser.url)
	
	return browser

def find(name = "", v = False):
	"""
	This will find the user page and return a dict of contact details.
	"""

	env = _loadENV()
	session = _login(env["rockUser"], env["rockPassword"])
	searchURL = "https://rock.newspring.cc/Person/Search/name/?SearchTerm="
	session.open(searchURL + name)
	if v: print(session.find_all("title"))

	#TODO if profile page pass that info back
	nameObj = session.find("h1", class_="title name")
	numListObj = session.find(class_="list-unstyled phonenumbers")
	emailListObj = session.find(class_="email")
	addrListObj = session.find(class_="list-unstyled margin-t-md")

	#format name
	fName = nameObj.find(class_="first-word").string
	lName = nameObj.find(class_="lastname").string
	name = fName + " " + lName
	
	# get list of numbers and format
	numList = []
	for num in numListObj.children:
		if num.name == "li":
			numType = num.contents[1].contents[0][0].lower()
			numPretty = numType + ": " + num.contents[0].strip()
			numList.append(numPretty)

	# get main email address
	email = "e: " + emailListObj.contents[1].string.strip()

	# get main home address
	for addr in addrListObj.contents[1]:
		if addr.string != None:
			continue
		if addr.attrs["class"][0] == "address":
			addrStr = addr.contents[0] + ", " + addr.contents[2]
			addrStr = "a: " + addrStr.strip()
			break

	# format and return SMS string
	sms = name + "\n"
	for num in numList:
		sms = sms + num + "\n"
	sms = sms + email + "\n" + addrStr
	return sms	

	#TODO if list of people, figure out who they need
	#TODO if no one comes up, reply back, can't find anyone

def _testSend(number = "", sms = "", creds = {}):
	"""
	Send the info back to the number.
	"""

	#TODO: use TwiML once debug is done
	# creds
	account = creds["twSID"]
	token = creds["twToken"]
	myNumber = creds["twNum"]

	client = Client(account, token)
	client.messages.create(
		to = number,
		from_ = myNumber,
		body = sms
	)

def _loadENV():
	"""
	Creates a dict of environment variables.
	"""
	
	dotenvPath = join(dirname(__file__), ".env")
	load_dotenv(dotenvPath)
	env = {}
	env["twSID"] = os.environ.get("TWILIO_ACCOUNT_SID")
	env["twToken"] = os.environ.get("TWILIO_AUTH_TOKEN")
	env["twNum"] = os.environ.get("TWILIO_NUMBER")
	env["rockUser"] = os.environ.get("ROCK_USER")
	env["rockPassword"] = os.environ.get("ROCK_PASSWORD")
	return env
	
if __name__ == "__main__":

	getContact("8036226599", "Greg DeMare", False)
	
