#!/usr/bin/env python
# -*- coding: utf-8 -*-

import functools

def func(x, y, z, t):
    return x, y, z, t

def bind(f, *pending_vals, **pending_params):
    @functools.wraps(func)
    def closure(*vals, **params):
        vals = pending_vals + vals
        params.update(pending_params)
        res = f(*vals, **params)
        return res
    return closure

f1 = bind(func, 1, 2, t=13)
assert f1([4]) == (1, 2, [4], 13)
