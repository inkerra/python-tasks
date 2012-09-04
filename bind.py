#!/usr/bin/env python
# -*- coding: utf-8 -*-

import functools

def func(x, y, z, t):
    return x, y, z, t

def bind(function, *pending_vals, **pending_params):
    @functools.wraps(function)
    def closure(*vals, **params):
        vals = pending_vals + vals
        params.update(pending_params)
        res = function(*vals, **params)
        return res
    return closure

if __name__ == "__main__":
	f1 = bind(func, 1, 2, t=13)
	assert f1([4]) == (1, 2, [4], 13)
