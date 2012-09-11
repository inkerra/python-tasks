#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from nose.tools import eq_

import sys
sys.path.insert(0, "../")

from rpc.rpc_client import RPCClient
from rpc.rpc_server import RPCServer
from rpc.common import MyRPC

import threading

class MainTestCase(unittest.TestCase):
	def setUp(self):
		pass

	def runTest(self):
		def run_server(ip, port):
			server = RPCServer(ip, port)
			server.register_function(lambda x, y: x + y, "add")
			server.register_function(lambda x: x, "same")
			def func1(x, a, b, c):
				return a * x ** 2 + b * x + c
			server.register_function(func1)
			try:
				server.run(10)
			except:
				pass

		def run_client(ip, port):
			client = RPCClient(ip, port)
			eq_([1], client.same([1]))
			slst = []
			for _ in range(1024 * 100):
				slst.append('a')
			ast = "".join(slst)
			self.assertEqual(len(ast), len(client.same(ast)))
			self.assertEqual(1, client.same(1))
			self.assertEqual(3, client.add(1, 2))
			self.assertEqual(11, client.func1(2, 1, 2, 3))
			self.assertEqual("Error: wrong argcount: add(1,), 2 expected", client.add(1))

		ip = ''
		port = 8000
		threads = []
		s = threading.Thread(None, run_server, "server", (ip, port))
		s.daemon = True
		threads.append(s)
		s.start()
		c = threading.Thread(None, run_client, "client", (ip, port))
		c.daemon = True
		threads.append(c)
		c.start()
		for th in threads:
			th.join()

	def tearDown(self):
		pass
