#!/usr/bin/env python
# -*- coding: utf-8 -*-

from types import FunctionType

ADD = lambda x, y: x + y
SUB = lambda x, y: x - y
MUL = lambda x, y: x * y
POW = lambda x, y: x ** y
DIV = lambda x, y: float(x) / y if y and x % y != 0 else x / y
FLOORDIV = lambda x, y: x // y
NEG = lambda x: -x

__is_binary_op = lambda f: f.func_code.co_argcount == 2

class ExpressionError(Exception):
    pass

def tree_gen(node):
    """ 
	generator of nodes for expression tree 
	for tree walking in order to calculate expression value
    """
    if node:
        if isinstance(node, Expression):
	    if node.op is not None:
		if __is_binary_op(node.op):
			yield node.op
	    	else:
		    yield node.op
		    for value in tree_gen(node.lf): yield value
		    return
	    for value in tree_gen(node.lf): yield value
	    for value in tree_gen(node.rg): yield value
	else: #ready value
	    yield node

def calculate(exp, **assigned_variables):
    """ calculate value of Expression exp,
	assigning variables from assigned_variables dictionary """
    for res in __calc(tree_gen(exp), **assigned_variables):
    	if res is None:
		raise ExpressionError("all variables should be assigned")
	return res
	
def __calc(it, **kwargs):
    for i in it:
	if isinstance(i, FunctionType):
	    lf = None
            for _ in __calc(it, **kwargs):
                lf = _
		break
            lv = __val(lf, **kwargs)
            if not __is_binary_op(i):
                yield __try_calc(i, lv)
		return

	    rg = None
	    for _ in __calc(it, **kwargs):
	        rg = _
		break
	    rv = __val(rg, **kwargs)
	    yield __try_calc(i, lv, rv)
	else: # variable or number
	    yield __val(i, **kwargs)

def __val(exp, **kwargs):
    if isinstance(exp, str): #Var
	if kwargs.has_key(exp):
		return kwargs[exp]
	return None
    else: #calculated value
	return exp

def __try_calc(func, *args):
    return None if reduce(lambda x, y: x or y is None, args, False) else func(*args)

class Expression(object):
    def __init__(self, lf, rg=None, op=None):
        self.lf = lf
        self.rg = rg
        self.op = op

    def __str__(self):
        return "({}, {}, {})".format(self.lf, self.rg, self.op)

    def __add__(self, x):
    	return Expression(self, x, ADD)
    
    def __radd__(self, x):
    	return Expression(x, self, ADD)
    
    def __sub__(self, x):
    	return Expression(self, x, SUB)

    def __rsub__(self, x):
    	return Expression(x, self, SUB)
    
    def __mul__(self, x):
    	return Expression(self, x, MUL)
    
    def __rmul__(self, x):
    	return Expression(x, self, MUL)

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

    def __neg__(self):
    	return Expression(self, None, NEG)
    
    def __call__(self, **kwargs):
	return calculate(self, **kwargs)

class Var(Expression):
    """ Leaf of the Expression Tree """
    pass 

def derivative(exp, dvar, **assigned_variables):
    """ calculate derivative of Expression exp,
	with respect to variable which name is dvar,
	assigning variables from assigned_variables dictionary """
    for res in __der_calc(tree_gen(exp), dvar, **assigned_variables):
	if res is None or res[1] is None:
		raise ExpressionError("unassigned variables in result expression")
        return res[1]

def __der_calc(it, dvar, **kwargs):
    for i in it:
	if isinstance(i, FunctionType):
	    lf = None
	    for _ in __der_calc(it, dvar, **kwargs):
		lf, dlf = _
		break
	    lv, dlv = __val(lf, **kwargs), __val(dlf, **kwargs)
	    if not __is_binary_op(i):
		yield __try_calc(i, lf), __try_calc(i, dlf)
		return
	    for _ in __der_calc(it, dvar, **kwargs):
		rg, drg = _
		break

	    rv, drv = __val(rg, **kwargs), __val(drg, **kwargs)
	    iv, idv = __try_calc(i, lv, rv), __try_calc(i, dlv, drv)

	    if i == MUL:
		lprod, rprod = 0 if drv == 0 else __try_calc(MUL, lv, drv), \
				0 if dlv == 0 else __try_calc(MUL, rv, dlv)
		yield (iv, __try_calc(ADD, lprod, rprod))
	    elif i == POW:
		yield (iv, __try_calc(MUL, dlv, \
			__try_calc(MUL, rv, __try_calc(POW, lv, (rv - 1)))))
	    elif i == DIV:
		yield (iv, \
			__try_calc(DIV, \
				__try_calc(MUL, dlv, rv) - \
				__try_calc(MUL, lv, drv), \
					__try_calc(POW, float(rv), 2)) )
	    elif i in {ADD, SUB}:
		yield (iv, idv)
	    else:
		raise ExpressionError("unsupported operation for derivation")
	else:
            yield __val(i, **kwargs), (i == dvar) if isinstance(i, str) else 0

if __name__ == "__main__":
    assert 1 == derivative(Var('x'), 'x')
    assert 10 == (1 + Var('x') * Var('x'))(x=3)
    assert 9 == (-Var('x')*-Var('x'))(x=3)
    assert 2 == (Var('x') // Var('y'))(x=5, y=2)
    assert 2.5 == (Var('x') / Var('y'))(x=5, y=2)
    assert (-2) == (-Var('x'))(x=2)
    assert (-1) == (1 + -Var('x'))(x=2)
    assert 10 == (7 + 9 * Var('x') - 2 * Var('y') + Var('z'))(y=2, x=1, z=-2)
    assert 10 == (1 + Var('x') * Var('x'))(x=3)
    assert 0 == derivative(Var('x'), 'y')
    assert 6 == derivative(1 + Var('x') * Var('x'), 'x', x=3)
    assert (-1) == derivative((- Var('x') - Var('y')),'y')
    assert (-4) == derivative(- Var('x') * Var('x') + Var('y'), 'x', x=2)
    try:
    	val = (- Var('x') ** Var('x') + Var('y'))(x=2)
    except ExpressionError:
	pass
    else:
	assert False
    assert (-1) == (- Var('x') ** Var('x') + Var('y'))(x=2, y=3)
    assert 6 * 2 ** 5 == derivative(Var('x') ** 6, 'x', x=2)
    assert (-3) == derivative((2 * Var('x') + 1) / (Var('x') - 1), 'x', x=2)
    assert (-1.5) == (- Var('x') / 2)(x=3)
    assert (-0.25) ==  derivative(1 / Var('x'), 'x', x=2)
    assert 21 ==  derivative((Var('x') ** 2 + 1) * (Var('x') + 2), 'x', x=2)
