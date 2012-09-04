#!/usr/bin/env python
# -*- coding: utf-8 -*-

def map_rq(func, iter):
    if len(iter) == 0: return []
    res = map_rq(func, iter[:-1])
    res.append(func(iter[-1]))
    return res

def map_yield(func, iter):
    for i in iter:
        yield func(i)

def map_rq_yield(func, iter):
    if len(iter) == 0:
        return
    yield func(iter[0])
    for i in map_rq_yield(func, iter[1:]):
        yield i
