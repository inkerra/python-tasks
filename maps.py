#!/usr/bin/env python
# -*- coding: utf-8 -*-

def map_rq(func, it):
    it = iter(it)
    for nxt in it:
    	res = [func(nxt)]
    	res.extend(map_rq(func, it))
    	return res
    else:
        return []

def map_yield(func, it):
    it = iter(it)
    for i in it:
        yield func(i)

def map_rq_yield(func, it):
    if it == None:
        return
    it = iter(it)
    yield func(next(it))
    for i in map_rq_yield(func, it):
        yield i

if __name__ == "__main__":
    def infinity_gen():
        i = 0
        while 1:
            yield i
            i += 1
    
    def gen(val):
        i = 0
        while i < val:
            yield i
            i += 1

    sq = lambda x: x ** 2

    print "map_rq works with generators:"
    for i in map_rq(sq, gen(4)):
        if i > 10:
            break
        print i
    print "map_yield works with infinity generators:"
    for i in map_yield(sq, infinity_gen()):
        if i > 10:
            break
        print i
    print "map_rq_yield works with infinity generators:"
    for i in map_rq_yield(sq, infinity_gen()):
        if i > 10:
            break
        print i
