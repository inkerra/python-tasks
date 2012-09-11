#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, "../")

from common import MyRPC

import socket

class RPCServer(MyRPC):
	def __init__(self, ip, port):
		super(RPCServer, self).__init__(ip, port)
		self.funcs = {}
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.s.bind((self.ip, self.port))
		self.s.listen(5)
	
	def register_function(self, function, name=None):
		if name is None: name = function.__name__
		self.funcs[name] = function

	def __call(self, name, *params):
		if self.funcs.has_key(name):
			f_argcount = self.funcs[name].func_code.co_argcount
			if f_argcount == len(params):
				try:
					return self.funcs[name](*params)
				except:
					return "Error: can't calculate function with params: {}{}".format(name, params)
			return "Error: wrong argcount: {}{}, {} expected".format(name, params, f_argcount)
		return "Error: unregistered function call: {}{}".format(name, params)

	def run(self, timeout=None):
		if timeout is not None:
			self.s.settimeout(timeout)

		while 1:
			try:
				while 1:
					self.conn, address = self.s.accept()
					data = self.read_msg()
					res = self.__call(*tuple(data))
					self.send_msg(res)
			except:
				raise
			finally:
				if self.__dict__.get("conn", None) is not None:
					self.conn.close()
