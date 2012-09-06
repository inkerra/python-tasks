# lambda-based solution
# closure-based sulition is almost the same

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
		
class Expression(object):
	def __init__(self, left, right=None, oper=None):
		self.left = left
		self.right = right
		self.oper = oper

	def __add__(self, x):
		return Expression(self, x, '+')

	def __sub__(self, x):
		return Expression(self, x, '-')

	def __mul__(self, x):
		return Expression(self, x, '*')

	def __radd__(self, x):
		return Expression(x, self, '+')

	def __rsub__(self, x):
		return Expression(x, self, '-')

	def __rmul__(self, x):
		return Expression(x, self, '*')

	def __neg__(self):
		return Expression(self, None, '--')

	def get_val(self, val, kwargs):
		if isinstance(val, Var):
			return kwargs[val.left]
		elif isinstance(val, Expression):
			return val(**kwargs)
		return val

	def __call__(self, **kwargs):
		lv = self.get_val(self.left, kwargs)
		if self.right is None:
			if self.oper == '--':
				return -lv
			assert False, "No right parameter for oper {!r}".format(self.oper)

		rv = self.get_val(self.right, kwargs)

		if self.oper == '+':
			return lv + rv
		elif self.oper == '-':
			return lv - rv
		elif self.oper == '*':
			return lv * rv

		assert False, "Unknown operator {!r}".format(self.oper)


class Var(Expression):
	pass

#print ((Var('x') + Var('y')) * 3 + 4 * Var('x'))(x=3, y=4)
#x = 3
#y = 4
#print (x + y) * 3 + 4 * x


# pythonic expression-based solution


import operator


class PyExpression_2(object):
	def __init__(self, left, right, oper):
		self.left = left
		self.right = right
		self.oper = oper

	def get_val(self, val, kwargs):
		if isinstance(val, PyExpression_2):
			return val(**kwargs)
		return val

	def __call__(self, **kwargs):
		return self.oper(self.get_val(self.left, kwargs), 
						 self.get_val(self.right, kwargs))

class PyExpression_1(PyExpression_2):
	def __init__(self, obj, oper):
		self.obj = obj
		self.oper = oper

	def __call__(self, **kwargs):
		return self.oper(self.get_val(self.obj, kwargs))

class PyVar(PyExpression_2):
	def __init__(self, name):
		self.name = name

	def __call__(self, **kwargs):
		return kwargs[self.name]

def method_1(func):
	def cl(self):
		return PyExpression_1(self, oper=func)
	return cl

def method_2(func):
	def cl(self, right):
		return PyExpression_2(self, oper=func, right=right)
	return cl

def method_r2(func):
	def cl(self, right):
		return PyExpression_2(right, oper=func, right=self)
	return cl

oper1_funcs = [
	operator.abs,
	operator.neg,
]

oper2_funcs = [
	operator.add,
	operator.sub,
	operator.div,
	operator.floordiv,
	operator.mul,
	operator.pow,
	operator.truediv,
	operator.mod,
	operator.rshift,
	operator.lshift,
	operator.eq,
	operator.ne,
	operator.le,
	operator.lt,
	operator.gt,
	operator.ge,
]

oper1_meth_name = {}
oper2_meth_name = {}

for func in oper1_funcs:
	oper1_meth_name[func] = '__{}__'.format(func.__name__)

for func in oper2_funcs:
	oper2_meth_name[func] = ('__{}__'.format(func.__name__),
							'__r{}__'.format(func.__name__))

oper2_meth_name[operator.and_] = ('__and__', '__rand__')
oper2_meth_name[operator.or_] = ('__or__', '__ror__')


for func, fname in oper1_meth_name.items():
	meth = method_1(func)
	meth.__name__ = fname
	setattr(PyExpression_2, fname, meth)

for func, (name, rname) in oper2_meth_name.items():
	meth = method_2(func)
	meth.__name__ = name
	setattr(PyExpression_2, name, meth)

	meth = method_r2(func)
	meth.__name__ = rname
	setattr(PyExpression_2, rname, meth)

#print PyExpression_2.__dict__.keys()

#x = PyVar('x')
#y = PyVar('y')

#print ((x & y) + x ** x)(x=33, y=2)

