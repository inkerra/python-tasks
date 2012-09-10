#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket 

class MyRPC(object):
	def __init__(self, ip, port):
		self.ip = ip
		self.port = port
		self.conn = None

	def send_msg(self, *data):
		msg = MyRPC.args_to_str(*data)
		self.conn.send(str(len(msg)) + '\n')
		self.conn.send(msg)

	def read_msg(self):
		size = int(self.get_msg(end='\n'))
		data = MyRPC.str_to_args(self.get_msg(size))
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
	
	__not_lst_to_lst = lambda x: [x] if not isinstance(x, list) else x
	
	@staticmethod
	def get_val(s):
		eq = s.find('=') # delimiter
		if eq == -1:
			raise MyFormatError('incorrect item: equal sign not found')
	
		itype = s[1:eq] # type
		t = s[eq:] # tail
		i = eq

		if itype == 'int':
			end = t.find('>')
			if end < 0:
				raise MyFormatError("invalid bracket expression")
			item = int(t[1:end])
		else: #str
			try:
				end = int(itype) + 1
			except:
				raise MyFormatError("incorrect type: '%s'", itype)
			if end > len(t): 
				raise MyFormatError("incorrect str type format: '%s'" % itype)
			item = t[1:end]
		return item, eq + end

	@staticmethod
	def str_to_args(s):
		if s == "": return []
	
		if s[0] == '<': # int or str value
			item, end = MyRPC.get_val(s)
			if end >= len(s):
				raise MyFormatError("incorrect item type format")
			return item
				
		elif s[0] == '[':
			i, idx = 1, -1
			buf = []
			args = []
			lstmode = False
			st = []
			while i + 1 < len(s):
				buf.append(s[i])
				if s[i] == '<':
					if lstmode:
						pass
					else:
						if buf == []:
							raise MyFormatError("invalid bracket expression")
						buf.pop()
						item, end = MyRPC.get_val(s[i:])
						i += end
						args.append(item)
				elif s[i] == '>':
					if lstmode:
						pass
					else:
						raise MyFormatError("invalid bracket expression")
				elif s[i] == '[':
					lstmode = True
					st.append(s[i])
				elif s[i] == ']':
					if st == []:
						raise MyFormatError("invalid bracket expression")
					st.pop()
					if st == []:
						lstmode = False
						argbuf = "".join(buf)
						if argbuf == "[]":
							lst = []
						else:
							lst = MyRPC.str_to_args(argbuf)
						buf = buf[:-len(argbuf)]
						args.append(lst)
				i += 1
			if buf != []:
				raise MyFormatError("invalid bracket expression")
				
			return args
		else: # neigther '[' nor '<'
			raise MyFormatError('item should be in angle brackets')
	
	@staticmethod
	def args_to_str(item):
		if isinstance(item, str):
			return "<%d=%s>" % (len(item), item)
		elif isinstance(item, int):
			return "<int=%d>" % item
		else:
			buf = []
			for e in item:
				buf.append(MyRPC.args_to_str(e))
			return "[%s]" % "".join(buf)

class MyFormatError(Exception):
	pass

if __name__ == "__main__":
	assert [']am]', [1]] == MyRPC.str_to_args("[<4=]am]>[<int=1>]]")
	#print "<am>:", repr(MyRPC.str_to_args("[<4=<am>>[<int=1>]]"))
	assert ['<am>', [1]] == MyRPC.str_to_args("[<4=<am>>[<int=1>]]")
	assert ['same', []] == MyRPC.str_to_args("[<4=same>[]]")
	assert [110, '1'] == MyRPC.str_to_args("[<int=110><1=1>]")
	assert ['add', 2, 3] == MyRPC.str_to_args("[<3=add><int=2><int=3>]")
	#print repr(MyRPC.str_to_args("[[[]<int=1>]<int=110>]"))
	#print repr(MyRPC.str_to_args("[[[]<int=1>[<int=0>]<7=abacaba>]<int=110>]"))
	assert [[[],1,[0],"abacaba"], 110] == MyRPC.str_to_args("[[[]<int=1>[<int=0>]<7=abacaba>]<int=110>]")
	assert 3 == MyRPC.str_to_args("<int=3>")
	assert "[<int=0>[<int=1><int=2>]<3=abc>]" == MyRPC.args_to_str([0, [1, 2], "abc"])
