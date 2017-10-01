#! usr/bin/python
# Copyright 2017 Michael Neeley
# This script will run unit tests on the rocksms app suite

import unittest
from rocksms import app

class TestRockSMS(unittest.TestCase):

	def test_message(self):
		
		# Use Flask's test client for our test
		self.testApp = app.test_client()

		# Make a test request to the sms app, supplying a fake number
		postData = {
			"From": "+15555555555",
			"Body": "Test"
		}
		response = self.testApp.post("/sms", data = postData)

		# Assert response is 200 OK
		self.assertEquals(response.status, "200 OK", "Response Data:\n" + response.data)
