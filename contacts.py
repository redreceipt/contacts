#! python3
# Copyright 2017 Michael Neeley
#
# This contains the main functions

###import requests, lxml.html
###from bs4 import BeautifulSoup
from robobrowser import RoboBrowser
###from base64 import b64decode, b64encode
import pdb

def main():
	"""
	Will get the contact info and send back to user.
	
	RETURNS:
		0 - Success.
	"""

	#TODO: login to Rock
	session = _login()

	#TODO: go find the person
	_find("Greg Demare", session, True)

	#TODO: send the info back

	return 0

def _login(user = "", pw = "", v = False):
	"""
	Will login using given credentials to Rock.
	"""

	loginPage = ("https://rock.newspring.cc")

	# testing robobrowser
	browser = RoboBrowser(history = True, parser = "lxml")
	browser.open(loginPage)
	#TODO find a better way to identify the form
	form = browser.get_forms()[0]
	#TODO: use dotenv to have environment variables
	form["ctl17$ctl01$ctl00$tbUserName"].value = "michael.neeley"
	form["ctl17$ctl01$ctl00$tbPassword"].value = "me2ee2cpe1!"
	submitBtn = "ctl17$ctl01$ctl00$btnLogin"
	browser.submit_form(form, submit = form[submitBtn])
	if v: print("Response URL: " + browser.url)
	
	return browser
	#pdb.set_trace()

def _find(name = "", session = None, v = False):
	"""
	This will find the user page and return a dict of contact details.
	"""
	
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
			numPretty = numType + " " + num.contents[0].strip()
			numList.append(numPretty)

	# get main email address
	email = emailListObj.contents[1].string.strip()

	# get main home address
	for addr in addrListObj.contents[1]:
		if addr.string != None:
			continue
		if addr.attrs["class"][0] == "address":
			addrStr = addr.contents[0] + ", " + addr.contents[2]
			addrStr = addrStr.strip()
			break

	# format and return SMS string
	sms = name + "\n"
	for num in numList:
		sms = sms + num + "\n"
	sms = sms + email + "\n" + addrStr
	return sms	

	#TODO if list of people, figure out who they need
	#TODO if no one comes up, reply back, can't find anyone

if __name__ == "__main__":
	
	print(main())
	
