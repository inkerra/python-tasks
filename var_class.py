#!/usr/bin/env python
# -*- coding: utf-8 -*-

import functools

def postponed(function):
    if len(function.func_code.co_varnames) != function.func_code.co_argcount:
	raise TypeError("can't decorate function with * or ** arguments in its signature")

    @functools.wraps(function)
    def closure(**params):
        fvarnames = function.func_code.co_varnames
            
        if len(params) == len(fvarnames):
            return function(**params)

        @functools.wraps(function)
        def closure1(**nparams):
            # skip already filled varnames (on previous steps)
            shift_filled = 0
            while shift_filled < len(fvarnames):
                if fvarnames[shift_filled] not in params.keys():
                    break
                shift_filled += 1

            # set fuction vars by new values (in new params dict)

            if params.viewkeys() & nparams.viewkeys():
                    raise ValueError("multiple values")

            nparams.update(params)

            return postponed(function)(**nparams)
        return closure1
        
    return closure
class Var(object):
    def __init__(self, name=None, value=None):
        self.name = name
        self.value = value

    def __call__(self, **params):
        self.known = params
        if self.name and self.known.has_key(self.name):
            self.value = self.known[self.name]
        return Var(value=self.value)

    def __str__(self):
        if self.value == None:
            return super(Var, self).__str__()
        return str(self.value)

    def __add__(self, other):
        return postponed(lambda x, y: x + y)

if __name__ == "__main__":
    x = Var('x')
    y = Var('y')

    func = x + y

    print func(x=3, y=2)

    func2 = x + x

    print func2(x=3)
