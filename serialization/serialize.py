#!/usr/bin/env python
# -*- coding: utf-8 -*-

import common

def serialize(item):
	if isinstance(item, str):
		return "<%d=%s>" % (len(item), item)
	elif isinstance(item, int):
		return "<int=%d>" % item
	elif isinstance(item, list):
		buf = []
		for e in item:
			buf.append(serialize(e))
		return "[%s]" % "".join(buf)
        else:
            raise SerializationError("unsupported type: " + type(item))

__all__ = ['serialize']

if __name__ == "__main__":
	assert "[<int=0>[<int=1><int=2>]<3=abc>]" == serialize([0, [1, 2], "abc"])
