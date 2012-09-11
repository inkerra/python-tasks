#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, "../")

from common import MyRPC

import socket
socket.setdefaulttimeout(60)

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
