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
