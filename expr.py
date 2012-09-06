#!/usr/bin/env python
# -*- coding: utf-8 -*-

ADD = lambda x, y: x + y
SUB = lambda x, y: x - y
MUL = lambda x, y: x * y
POW = lambda x, y: x ** y
DIV = lambda x, y: float(x) / y if y and x % y != 0 else x / y
FLOORDIV = lambda x, y: x // y
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

	def __rpow__(self, x):
                return Expression(x, self, POW)

	def __div__(self, x):
                return Expression(self, x, DIV)

	def __rdiv__(self, x):
                return Expression(x, self, DIV)

	def __floordiv__(self, x):
                return Expression(self, x, FLOORDIV)

	def __rfloordiv__(self, x):
                return Expression(x, self, FLOORDIV)

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
    print (2 ** Var('x'))(x=3)
    print (7 / Var('x'))(x=3)
    print (4 // Var('x'))(x=3)
