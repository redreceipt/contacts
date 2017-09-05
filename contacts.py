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
	_login()

	#TODO: go find the person

	#TODO: send the info back

	return 0

def _login(user = "", pw = ""):
	"""
	Will login using given credentials to Rock.
	"""

	loginPage = ("https://rock.newspring.cc")

	# testing robobrowser
	browser = RoboBrowser(history = True)
	browser.open(loginPage)
	form = browser.get_forms()[0]
	#TODO: use dotenv to have environment variables
	form["ctl17$ctl01$ctl00$tbUserName"].value = "michael.neeley"
	form["ctl17$ctl01$ctl00$tbPassword"].value = "me2ee2cpe1!"
	submitBtn = "ctl17$ctl01$ctl00$btnLogin"
	browser.submit_form(form, submit = form[submitBtn])
	print("robobrowser: " + browser.url)
	
	#pdb.set_trace()

if __name__ == "__main__":
	
	print(main())
