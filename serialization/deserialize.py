#!/usr/bin/env python
# -*- coding: utf-8 -*-

import common

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
		if end > len(t): 
			raise SerializationError("incorrect str type format: '%s'" % itype)
		item = t[1:end]
	return item, eq + end

def deserialize(s):
	if s == "": return []

	if s[0] == '<': # int or str value
		item, end = get_val(s)
		if end >= len(s):
			raise SerializationError("incorrect item type format")
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
						raise SerializationError("invalid bracket expression")
					buf.pop()
					item, end = get_val(s[i:])
					i += end
					args.append(item)
			elif s[i] == '>':
				if lstmode:
					pass
				else:
					raise SerializationError("invalid bracket expression")
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
                        print buf
			raise SerializationError("invalid bracket expression")
			
		return args
	else: # neigther '[' nor '<'
		raise SerializationError('item should be in angle brackets')

__all__ = ['deserialize']

if __name__ == "__main__":
	assert [']am]', [1]] == deserialize("[<4=]am]>[<int=1>]]")
        assert [[1], ["ss", 2], [[[[1]]], [2,[3,"12"]]]] ==  deserialize("[[<int=1>][<2=ss><int=2>][[[[<int=1>]]][<int=2>[<int=3><2=12>]]]]")
	assert [']am]', [[[1]]]] == deserialize("[<4=]am]>[[[<int=1>]]]]")
	#print "<am>:", repr(deserialize("[<4=<am>>[<int=1>]]"))
	assert ['<am>', [1]] == deserialize("[<4=<am>>[<int=1>]]")
	assert ['same', []] == deserialize("[<4=same>[]]")
	assert [110, '1'] == deserialize("[<int=110><1=1>]")
	assert ['add', 2, 3] == deserialize("[<3=add><int=2><int=3>]")
	#print repr(deserialize("[[[]<int=1>]<int=110>]"))
	#print repr(deserialize("[[[]<int=1>[<int=0>]<7=abacaba>]<int=110>]"))
	assert [[[],1,[0],"abacaba"], 110] == deserialize("[[[]<int=1>[<int=0>]<7=abacaba>]<int=110>]")
	assert 3 == deserialize("<int=3>")
