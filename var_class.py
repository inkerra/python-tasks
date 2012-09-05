#!/usr/bin/env python
# -*- coding: utf-8 -*-

class decor:
	def __init__(self, func):
		self.func = func

	def __call__(self, *args, **kwargs):
		print args
		print kwargs
		self.func(*args, **kwargs)

@decor
class Var(object):
    def __init__(self, name=None, value=None, saved=None):
	self.name = name
	self.value = value
	self.saved = saved

    def __call__(self, **params):
        known = self.saved if self.saved else {}
	known.update(params)
        if self.name and known.has_key(self.name):
        	return Var(name=self.name, value=known[self.name])
	return Var(name=self.name, saved=known)

    def __str__(self):
        if self.value == None:
            return super(Var, self).__str__()
        
        return super(Var, self).__str__() + ": " +  str(self.value)

    def __add__(self, other):
	
	return Var({self.name: self.value, other.name: other.value})

if __name__ == "__main__":
    x = Var('x')
    y = Var('y')

    print x
    print x(x=1)
    print x(z=1, x=2)(x=3)
    #xx = x(x=1)
    #yy = y(y=2)

    #print xx + yy
    #func x + y

    #print func(x=3, y=2)

    #func2 = x + x

    #print func2(x=3)
