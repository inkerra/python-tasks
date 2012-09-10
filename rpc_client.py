#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
socket.setdefaulttimeout(5)
from rpc import MyRPC

class RPCClient(MyRPC):
	def __getattr__(self, name):
		def cb(*args):
			self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.conn.connect((self.ip, self.port))
			try:
				self.send_msg([name] + list(args))
				return self.read_msg()
			except:
				raise
			finally:
				self.conn.close()
		return cb

if __name__ == "__main__":
	c = RPCClient("localhost", 8000)
	assert [1] == c.same([1])
	assert 1 == c.same(1)
	assert 3 == c.add(1, 2)
	assert 11 == c.func1(2, 1, 2, 3)
	#incorrect function call
	assert "Error: wrong argcount: add(1,), 2 expected" == c.add(1)
