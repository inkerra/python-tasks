#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Var(object):
	def __init__(self, val=None):
		self.val = val

	def __call__(self):
		return self.val

	def __str__(self):
		return str(self.val)

	def __add__(self, other):
		return Var(val = self.val + other.val)

	def __mul__(self, other):
		return Var(val = self.val * other.val)

	def __setattr__(self, name, val):
		self.__dict__[name] = 0 if val is None else val

if __name__ == "__main__":
	x = Var(2)
	y = Var(3)
	print x + x
	#print x + x + x
	#print x * y + x + x
