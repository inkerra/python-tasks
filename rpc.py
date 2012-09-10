#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket 
from serialization.serialize import serialize
from serialization.deserialize import deserialize

class MyRPC(object):
	def __init__(self, ip, port):
		self.ip = ip
		self.port = port
		self.conn = None

	def send_msg(self, *data):
		msg = serialize(*data)
		self.conn.send(str(len(msg)) + '\n')
		self.conn.send(msg)

	def read_msg(self):
		size = int(self.get_msg(end='\n'))
		data = deserialize(self.get_msg(size))
		return data

	def get_msg(self, size=None, end=None):
		if size is not None:
			res = self.conn.recv(size) #fixme
			if res < size:
				res += self.get_msg(size - res)
			return res
		
		if end is not None:
			buf = []
			i = 0
			while True:
				c = self.conn.recv(1)
				if c == end:
					return "".join(buf)
				else:
					buf.append(c)
				i += 0
