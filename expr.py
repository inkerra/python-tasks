#!/usr/bin/env python
# -*- coding: utf-8 -*-

def get_val(x, kwargs):
	if isinstance(x, Expression_L):
		return x(**kwargs)
	return x
	
class Expression_L(object):
	def __init__(self, func):
		self.left = left
		self.right = right
		self.oper = oper

	def __add__(self, x):
		return lambda **kwargs : self(**kwargs) + get_val(x, kwargs) 

	def __radd__(self, x):
		return lambda **kwargs : get_val(x, kwargs) + self(**kwargs)

	def __neg__(self):
		return lambda **kwargs : -self(**kwargs)

class Var_L(Expression_L):
	def __init__(self, name):
		Expression_L.__init__(lambda **kwargs: kwargs[name])
		

# Basic expression-based solution

ADD = lambda x, y: x + y
SUB = lambda x, y: x - y
MUL = lambda x, y: x * y
POW = lambda x, y: x ** y
NEG = lambda x: -x
		
class Expression(object):
	def __init__(self, left, right=None, oper=None):
		self.left = left
		self.right = right
		self.oper = oper

	def __add__(self, x):
		return Expression(self, x, ADD)

	def __sub__(self, x):
		return Expression(self, x, SUB)

	def __mul__(self, x):
		return Expression(self, x, MUL)

	def __pow__(self, x):
                return Expression(self, x, POW)

	def __radd__(self, x):
		return Expression(x, self, ADD)

	def __rsub__(self, x):
		return Expression(x, self, SUB)

	def __rmul__(self, x):
		return Expression(x, self, MUL)

	def __neg__(self):
		return Expression(self, None, NEG)

	def get_val(self, val, kwargs):
		if isinstance(val, Var):
			return kwargs[val.left]
		elif isinstance(val, Expression):
			return val(**kwargs)
		return val

	def __call__(self, **kwargs):
            if self.right is None and self.oper is None:
                return self.get_val(self, kwargs)

            lf = self.get_val(self.left, kwargs)

            if self.right is None and self.oper is not None:
                return self.oper(lf)

            if self.right is None:
                return lf

            rg = self.get_val(self.right, kwargs)

            return self.oper(lf, rg)

        def derivative(self):
            return None

class Var(Expression):
	pass

if __name__ == "__main__":
    x, y = 3, 4
    assert ((Var('x') + Var('y')) * 3 + 4 * Var('x'))(x=3, y=4) == (x + y) * 3 + 4 * x
    print (Var('x') ** 2)(x=3)
