#!/usr/bin/env python
# -*- coding: utf-8 -*-

import functools
import types

def check_me(function):
	if len(function.func_code.co_varnames) != function.func_code.co_argcount:
		raise TypeError("can't decorate function with * or ** arguments in its signature")

	@functools.wraps(function)
	def closure(*vals, **params):
		# generate dict with type restrictions from docstring
		# return dist: key = varname, value = vartype from function's docstring
		def _gen_restr(docstring):
			doclines = [ s.strip() for s in docstring.splitlines() if len(s.strip())]
			paramprefix = "@param "
			paramlines = filter(lambda s: s.startswith(paramprefix), doclines)
			paramlst = [s.replace(paramprefix, "", 1).split(":", 1) for s in paramlines]
			restr = {}
			for s in paramlines:
				p = s.replace(paramprefix, "", 1).split(":", 1) 
				if len(p) == 2:
					p = [s.strip() for s in p]
					restr[p[0]] = p[1]
			return restr

		restr = _gen_restr(function.func_doc)

		# set function' vals to params
		varnames = function.func_code.co_varnames
        	j = 0
        	for varname in varnames:
                    if varname not in params.keys():
			if j >= len(vals):
				raise TypeError("wrong args number")
                        
			if varname not in restr.keys() or repr(type(vals[j])) == "<type '%s'>" % restr[varname]:
                    		params[varname] = vals[j]
			else:
				# FIXME if it should be TypeError as in task
				# (but there is ValueError in the unittest checker)
        			raise ValueError('{} is not a {}'.format(repr(type(vals[j])), "<type '%s'>" % restr[varname]))
			j += 1
                    else:
			if j < len(vals): # we must set vals before params
                        	raise ValueError("got multiple values for keyword argument")
                if j < len(vals):
                    raise ValueError("got too much values for keyword argument")
		del vals
            
                if len(params) == len(varnames):
		    return function(**params)
		else:
		    raise TypeError("wrong args number")

	return closure

if __name__ == "__main__":
	@check_me
	def my_func(x, y, z, dummy, func):
	    """
	    @param x: int
	    @param y: str
	    @param z: float
	    @param func: function
	    """
	    #print func.__name__
	    return x + int(y) + float(z)
	
	assert my_func(2, dummy="some string", z=0, func=my_func, y="3") == 5
