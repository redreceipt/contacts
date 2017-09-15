#! python3
# Copyright 2017 Michael Neeley
#
# This contains the main functions

# built-in libs
import os, argparse
from os.path import join, dirname

# installed libs
from robobrowser import RoboBrowser # pip install robobrowser
from twilio.rest import Client # pip install twilio
from twilio.base.exceptions import TwilioRestException
from dotenv import load_dotenv # pip install -U python-dotenv

###from base64 import b64decode, b64encode
import pdb

# Globals
VERBOSE = False
PROFILE_URL = "http://rock.newspring.cc/Person/"
LOGIN_URL = "https://rock.newspring.cc"
USER_FIELD_ID = "ctl17$ctl01$ctl00$tbUserName"
PW_FIELD_ID = "ctl17$ctl01$ctl00$tbPassword"
LOGIN_BTN_ID = "ctl17$ctl01$ctl00$btnLogin"
SEARCH_URL = "https://rock.newspring.cc/Person/Search/name/?SearchTerm="
PEOPLE_TBL_ID = "ctl00_main_ctl09_ctl01_ctl00_gPeople"

def _main(query = "", to = None):
	"""
	Will get the contact info and send back to user.
	"""

	msg = search(query)
	if to: _sendMessage(to, msg)
	return msg

def _login(user = "", pw = ""):
	"""
	Will login using given credentials to Rock.
	"""

	loginPage = (LOGIN_URL)

	# testing robobrowser
	browser = RoboBrowser(history = True, parser = "lxml")
	browser.open(loginPage)
	form = browser.get_forms()[0]
	form[USER_FIELD_ID].value = user
	form[PW_FIELD_ID].value = pw
	submitBtn = LOGIN_BTN_ID
	browser.submit_form(form, submit = form[submitBtn])
	
	return browser

def search(query = ""):
	"""
	This will find the user page and return a dict of contact details.
	"""

	# login to Rock
	env = _loadENV()
	session = _login(env["rockUser"], env["rockPassword"])
	
	# get name and filters
	args = query.split()
	filters = []
	while len(args) > 2:
		filters.append(args.pop())
	name = " ".join(args)
	
	session.open(SEARCH_URL + name)

	# found
	if "Person Search" not in session.find("title").string:
		return _getInfo(session)

	# either not found or multiples found
	options = _getOptions(session, name, filters)

	# not found
	if -1 in options.keys():
		return options[-1]

	# found person based on filters	
	if len(options) == 1:
		return _getInfo(session, list(options.keys())[0])

	# if there are multiple options, tell the user to add filters
	reply = str(len(options)) + " options found for \"" + name + "\". "
	reply += "Try adding one or more of these filters...\n\n"
	allOptions = []
	for key in options.keys():
		allOptions += options[key]
	prettyOptions = ", ".join(list(set(allOptions)))
	return reply + prettyOptions

def _getOptions(session = None, name = "", filters = []):
	"""
	This will return a list of options to choose from.
	"""

	peopleTableID = PEOPLE_TBL_ID
	peopleTable = session.find_all("table", id = peopleTableID)
	peopleRows = peopleTable[0].find_all("tr")
	
	# respond back if no one is found
	if peopleRows[1].find("td").string == "No People Found":
		msg = str("\"" + name + "\" not found, check spelling")
		return {-1: msg}

	# remove rows in the table that aren't people
	peopleRows.pop(0)
	peopleRows.pop()
	options = {}
	for row in peopleRows:
		
		# set row key to find person later
		try:
			key = row.attrs["datakey"]
		except KeyError:
			pass
	
		# get the strings inside the td tags
		data = list(map(
			lambda x: unicode(x.string).strip().strip("()"),
			row.find_all("td")))
		
		# add the strings from the small tags
		data += list(map(
			lambda x: unicode(x.string).strip().strip("()"),
			row.find_all("small")))
	
		# remove birthdays
		data = list(filter(
			lambda x: "/" not in x,
			data))
			
		# remove empty cells
		data = list(filter(
			lambda x: x != "None" and x.strip() != "",
			data))
	
		# if rows are blank, don't add as options
		if data == []: continue

		# check data against filters
		data.append("")
		if set(filters).issubset(set(data)):
			data.pop()
			options[key] = data

	if options == {}:
		msg = "No results for \"" + name + "\" matched your filters"
		return {-1: msg}

	return options
	
def _getInfo(session = None, personKey = None):
	"""
	This will return a string of the contact info.
	"""
	
	# if personKey is defined we want a specific person
	if personKey: session.open(PROFILE_URL + personKey)

	nameObj = session.find("h1", class_="title name")
	numListObj = session.find(class_="list-unstyled phonenumbers")
	emailListObj = session.find(class_="email")
	addrListObj = session.find(class_="list-unstyled margin-t-md")

	#format name
	fName = nameObj.find(class_="first-word").string
	lName = nameObj.find(class_="lastname").string
	name = fName + " " + lName
	
	# get list of numbers and format
	# TODO: use find_all instead of iterating through
	numList = []
	for num in numListObj.children:
		if num.name == "li":
			numType = num.contents[1].contents[0][0].lower()
			numPretty = numType + ": " + num.contents[0].strip()
			numList.append(numPretty)

	# get main email address
	email = "e: " + emailListObj.contents[1].string.strip()

	# get main home address
	# TODO: use find_all instead of iterating through
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


def _sendMessage(to = "", body = ""):
	"""
	Send a message using Twilio REST API.
	"""

	# creds
	creds = _loadENV()
	account = creds["twSID"]
	token = creds["twToken"]
	from_ = creds["twNum"]

	client = Client(account, token)
	client.messages.create(
		to = to,
		from_ = from_,
		body = body
	)

def _loadENV():
	"""
	Creates a dict of environment variables.
	"""

	#TODO: authenticate before, else respond you can't	
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

	# create argument parser
	parser = argparse.ArgumentParser(
		description = "Sends Rock users contact info.")
	parser.add_argument("search", 
		help = "name and info to search for")
	parser.add_argument("--to",
		help = "number to send response to")
	parser.add_argument("-v", "--verbose",
		help = "prints extra debug info",
		action = "store_true")
	args = parser.parse_args()

	VERBOSE = args.verbose
	print(_main(args.search, args.to))
	
