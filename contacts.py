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
###	headers={"User-Agent":"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36"}

	# create a new session
###	s = requests.session()
###	s.headers.update(headers)
###	page = s.get(loginPage)
###	soup = BeautifulSoup(page.content, "lxml")
	#pageHTML = lxml.html.fromstring(page.text)

	# grab ASP.NET __VIEWSTATE strings
###	VIEWSTATE=soup.find(id="__CVIEWSTATE")['value']
	#VIEWSTATEGENERATOR=soup.find(id="__VIEWSTATEGENERATOR")['value']
###	EVENTVALIDATION=soup.find(id="__EVENTVALIDATION")['value']

	#form = {x["name"]: x["value"] for x in soup.findAll(type = "hidden")}	
###	form = {}
	
	#TODO: find all hidden inputs in the login form
	#pdb.set_trace()
	"""
	hidden = soup.findAll(type = "hidden")
	for x in hidden:
		if x.has_attr("value"):
			form[x["name"]] = x["value"]
	"""
###	form["__VIEWSTATE"] = VIEWSTATE
	#TODO: use dotenv to have environment variables
###	form = {
	#"__CVIEWSTATE":VIEWSTATE,
###	"__CVIEWSTATE": VIEWSTATE,
	#"__VIEWSTATEGENERATOR":VIEWSTATEGENERATOR,
###	"__EVENTVALIDATION":EVENTVALIDATION,
###	}
###	form["ctl17$ctl01$ctl00$tbUserName"] = "michael.neeley"
###	form["ctl17$ctl01$ctl00$tbPassword"] = "me2ee2cpe1!"

###	response = s.post(loginPage, data = form)

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
	
###	print(response.url)	
	#pdb.set_trace()

if __name__ == "__main__":
	
	print(main())
