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
	
	def send_msg(self, data):
		super(RPCServer, self).send_msg(data)

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

	def run(self):
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
				self.conn.close()

if __name__ == "__main__":
	def func1(x, a, b, c):
		return a * x ** 2 + b * x + c
		
	srv = RPCServer("localhost", 8000)
	srv.register_function(lambda x, y: x + y, "add")
	srv.register_function(lambda x: x, "same")
	srv.register_function(func1)
	srv.run()
