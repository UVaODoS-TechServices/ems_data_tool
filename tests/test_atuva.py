#! /usr/bin/env python
# -*- coding: utf-8 -*-

""" Unittests for atuva library. """

import random
import time
import types
import unittest

from ConfigParser import SafeConfigParser

from lib.atuva import create_hash, create_random, get_current_time, make_request, get_items

class TestAtUVa(unittest.TestCase):
	""" Tests for validating atuva library. """
	
	def test_create_hash(self):
		""" Tests ability to create secure message hash. """
		
		args = ("foo", "bar", "baz", "qux",) #fudge arg tuple
		
		result = create_hash(*args)
		
		self.assertIsInstance(result, str)
		self.assertEqual(len(result), 32)
	
	def test_create_random(self):
		""" Tests ability to successfully create random. """
		
		result = create_random()
		other = create_random() #something for the comparison?
		
		self.assertIsInstance(result, str)
		self.assertEqual(len(result), 32)
		self.assertNotEqual(result, other)
	
	def test_get_current_time(self):
		""" Tests ability to produce current time in milliseconds. """
		
		result = get_current_time()
		curtime = str(int(round(time.time() * 1000)))
		
		self.assertIsInstance(result, str)
		self.assertEqual(result, curtime)
	
	def test_make_request(self):
		""" Tests ability to produce result of RESTful request. """
		
		config = SafeConfigParser()
		config.optionxform(str())
		config.read("./config/settings.ini")
		
		resource = "test"
		params = {}
		session = None
		headers = {"Content-Type": "application/json"}
		
		result = make_request(config, resource, params, session, headers)
		
		self.assertTrue(result.ok)
		self.assertEqual(result.json()['totalPages'], 0)
		self.assertTrue('test' or 'Test' in result.json()['items'])
	
	def test_get_items(self):
		""" Tests ability to request and paginate RESTful request response. """
		
		config = SafeConfigParser()
		config.optionxform(str())
		config.read("./config/settings.ini")
		
		resource = "test"
		params = {}
		session = None
		headers = {"Content-Type": "application/json"}
		
		result = get_items(config, resource, params, session, headers)
		
		self.assertIsInstance(result, types.GeneratorType)
		
		try:
			list(result)
			flag = True
		
		except Exception:
			flag = False
		
		self.assertTrue(flag)


if __name__ == "__main__":
	pass
