#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from nose.tools import eq_

import sys
sys.path.insert(0, "../")

from rpc.rpc_client import RPCClient
from rpc.rpc_server import RPCServer
from rpc.common import MyRPC

class MainTestCase(unittest.TestCase):
    def setUp(self):
        self.server = RPCServer('', 8000)
        self.server.register_function(lambda x, y: x + y, "add")
        self.server.register_function(lambda x: x, "same")
        def func1(x, a, b, c):
    	    return a * x ** 2 + b * x + c
        self.server.register_function(func1)
        self.server.run()
        self.client = RPCClient('', 8000)
    
    def runTest(self):
        self.assertEqual([1], client.same([1]))
        self.assertEqual(1, client.same(1))
        self.assertEqual(3, client.add(1, 2))
        self.assertEqual(11, client.func1(2, 1, 2, 3))
        self.assertEqual("Error: wrong argcount: add(1,), 2 expected", client.add(1))
    
    def tearDown(self):
        pass
