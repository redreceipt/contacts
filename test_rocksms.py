#! usr/bin/python
# Copyright 2017 Michael Neeley
# This script will run unit tests on the rocksms app suite

import logging
import unittest
from xml.etree import ElementTree as ET

from rocksms import app

# disable logging
#TODO: turn off logging for file but set console to debug
logging.disable(logging.WARNING)

class TwiMLTest(unittest.TestCase):
		def setUp(self):
			self.client = app.test_client()

		def assertTwiML(self, response):
			self.assertEquals(response.status, "200 OK")
			x = ET.fromstring(response.data)
			self.assertEquals(x.tag, "Response", "Did not get back a TwiML Response tag.")

		def call(self, url = "/voice", from_ = "+15556667777",
			digits = None, extra_params = None):
			"""
			Simulates Twilio Voice request to Flask test client.
			"""

			# Set some common parameters for messages received by Twilio.
			params = {
				"CallSid": "CAtesting",
				"AccountSid": "ACxxxxxxxxxxxxx",
				"To": "+15551234567",
				"From": from_,
				"CallStatus": "ringing",
				"Direction": "inbound",
				"FromCity": "BROOKLYN",
				"FromState": "NY",
				"FromCountry": "US",
				"FromZip": "55555"}
 
			# Add simulated DTMF input.
			if digits:
				params["Digits"] = digits
 
			# Add extra params not defined by default.
			if extra_params:
				params = dict(params.items() + extra_params.items())
 
			# Return the app's response.
			return self.client.post(url, data = params)

		def message(self, body, url = "/sms", from_ = "+15556667777", extra_params = None):
			"""
			Simulates Twilio Message request to Flask test client.
			"""

			# Set some common parameters for messages received by Twilio.
			params = {
				"MessageSid": "SMtesting",
				"AccountSid": "ACxxxxxxxxxxxxx",
				"To": "+15551234567",
				"From": from_,
				"Body": body,
				"NumMedia": 0,
				"FromCity": "BROOKLYN",
				"FromState": "NY",
				"FromCountry": "US",
				"FromZip": "55555"}
 
			# Add extra params not defined by default.
			if extra_params:
				params = dict(params.items() + extra_params.items())
 
			# Return the app's response.
			return self.client.post(url, data = params)

class ContactsSearchTest(TwiMLTest):

	def test_inactiveEmail(self):
		body = "John Doe"
		response = self.message(body)
		self.assertTwiML(response)
