#!/usr/bin/env python
# -*- coding: utf-8 -*-

from common import SerializationError

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
            raise SerializationError("unsupported type: {} ".format(type(item)))

__all__ = ['serialize']
