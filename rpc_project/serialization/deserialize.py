#!/usr/bin/env python
# -*- coding: utf-8 -*-

from common import SerializationError

def get_val(s):
	eq = s.find('=') # delimiter
	if eq == -1:
		raise SerializationError('incorrect item: equal sign not found')

	itype = s[1:eq] # type
	t = s[eq:] # tail
	i = eq

	if itype == 'int':
		end = t.find('>')
		if end < 0:
			raise SerializationError("invalid bracket expression")
		item = int(t[1:end])
	else: #str
		try:
			end = int(itype) + 1
		except:
			raise SerializationError("incorrect type: '%s'", itype)
		item = t[1:end]
	return item, eq + end

def deserialize(s):
	if s == "": return []

	if s[0] == '<': # int or str value
		item, end = get_val(s)
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
				if not lstmode:
					buf.pop()
					item, end = get_val(s[i:])
					i += end
					args.append(item)
			elif s[i] == '[':
				lstmode = True
				st.append(s[i])
			elif s[i] == ']':
                                if st == []:
			            raise SerializationError("invalid bracket expression")

				st.pop()
				if st == []:
					lstmode = False
					argbuf = "".join(buf)
					if argbuf == "[]":
						lst = []
					else:
						lst = deserialize(argbuf)
					buf = buf[:-len(argbuf)]
					args.append(lst)
			i += 1
		if buf != []:
			raise SerializationError("invalid bracket expression")
			
		return args
	else: # neigther '[' nor '<'
		raise SerializationError('item should be in angle brackets')

__all__ = ['deserialize']
