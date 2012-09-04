#!/usr/bin/env python
# -*- coding: utf-8 -*-

import functools

def me_haskell(f, *h_vals, **h_params):
    if h_vals != () or h_params != {}:
        raise ValueError("decorator must not have vals or params")
    
    @functools.wraps(f)
    def closure(*vals, **params):
        fvarnames = f.func_code.co_varnames
        if len(fvarnames) < len(vals):
            raise ValueError("got too much values for keyword argument")

        i, j = 0, 0
        while i < len(fvarnames) and j < len(vals):
            if not params.has_key(fvarnames[i]):
                params[fvarnames[i]] = vals[j]
                j += 1
            else:
                raise ValueError("got multiple values for keyword argument")
            i += 1
            
        if j < len(vals):
            raise ValueError("got too much values for keyword argument")
            
        if len(params) == len(fvarnames):
            return f(**params)

        @functools.wraps(f)
        def closure1(*nvals, **nparams):
            # skip already filled varnames (on previous steps)
            shift_filled = 0
            while shift_filled < len(fvarnames):
                if not params.has_key(fvarnames[shift_filled]):
                    break
                shift_filled += 1

            # set fuction vars by new values (in new params dict)
            i, j = shift_filled, 0
            while i < len(fvarnames) and j < len(nvals):
                varname = fvarnames[i]
                # set function var by current new value if var hasn't been set
                if not params.has_key(varname) and not nparams.has_key(varname):
                    nparams[varname] = nvals[j]
                    i += 1
                else:
                    raise ValueError("got multiple values for keyword argument")
                j += 1

            if j < len(nvals):
                raise ValueError("got too much values for keyword argument")
            nvals = {}

            # check if key has been already filled
            for key in params.keys():
                if nparams.has_key(key):
                    raise ValueError("multiple values")

            nparams.update(params)

            return me_haskell(f)(*nvals, **nparams)
        return closure1
        
    return closure

@me_haskell
def func(x, y, z):
    return x, y, z

f1 = func(1)
assert f1(2, 3) == (1, 2, 3)

f2 = f1(z = True)
assert f2("abc") == (1, "abc", True)

try:
    func(1, x=1)
    assert False, "exception should be raised"
except:
    pass

try:
    func(1, 2)(y=1)
    assert False, "exception should be raised"
except:
    pass

try:
    func(y=12)(1, 2)
    assert False, "exception should be raised"
except:
    pass

assert func(y=12)(1, z=2) == (1, 12, 2)
