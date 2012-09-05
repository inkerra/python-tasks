#!/usr/bin/env python
# -*- coding: utf-8 -*-

import functools

def me_haskell(function):
    if len(function.func_code.co_varnames) != function.func_code.co_argcount:
	raise TypeError("can't decorate function with * or ** arguments in its signature")

    @functools.wraps(function)
    def closure(*vals, **params):
        fvarnames = function.func_code.co_varnames
        if len(fvarnames) < len(vals):
            raise ValueError("got too much values for keyword argument")

        i, j = 0, 0
        while i < len(fvarnames) and j < len(vals):
            if fvarnames[i] not in params.keys():
                params[fvarnames[i]] = vals[j]
                j += 1
            else:
                raise ValueError("got multiple values for keyword argument")
            i += 1
            
        if j < len(vals):
            raise ValueError("got too much values for keyword argument")
            
        if len(params) == len(fvarnames):
            return function(**params)

        @functools.wraps(function)
        def closure1(*nvals, **nparams):
            # skip already filled varnames (on previous steps)
            shift_filled = 0
            while shift_filled < len(fvarnames):
                if fvarnames[shift_filled] not in params.keys():
                    break
                shift_filled += 1

            # set fuction vars by new values (in new params dict)
            i, j = shift_filled, 0
            while i < len(fvarnames) and j < len(nvals):
                varname = fvarnames[i]
                # set function var by current new value if var hasn't been set
                if varname not in params.keys() and varname not in nparams.keys():
                    nparams[varname] = nvals[j]
                    i += 1
                else:
                    raise ValueError("got multiple values for keyword argument")
                j += 1

            if j < len(nvals):
                raise ValueError("got too much values for keyword argument")
            del nvals

            if params.viewkeys() & nparams.viewkeys():
                    raise ValueError("multiple values")

            nparams.update(params)

            return me_haskell(function)(**nparams)
        return closure1
        
    return closure

if __name__ == "__main__":
	@me_haskell
	def func(x, y, z):
	    return x, y, z

	try:
	    @me_haskell
	    def func2(x, *y):
	        return (x, y)

	    assert False

	    func2(1, 2, 3, 4)
	except TypeError:
	    pass
	
	f1 = func(1)
	assert f1(2, 3) == (1, 2, 3)
	
	f2 = f1(z = True)
	assert f2("abc") == (1, "abc", True)
	
	try:
	    func(1, x=1)
	    assert False, "exception should be raised"
	except ValueError:
	    pass
	
	try:
	    func(1, 2)(y=1)
	    assert False, "exception should be raised"
	except ValueError:
	    pass

	try:
	    func(x=1)(x=1)
	    assert False, "exception should be raised"
	except ValueError, e:
            assert e.message == "multiple values"
	
	try:
	    func(y=12)(1, 2)
	    assert False, "exception should be raised"
	except ValueError:
	    pass
	
	assert func(y=12)(1, z=2) == (1, 12, 2)
