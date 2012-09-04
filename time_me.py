#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import functools

statistic = {}

def time_me(timer, stats):
    def closure0(func):
        @functools.wraps(func)
        def closure(*vals, **params):
            start = timer()
            res = func(*vals, **params)
            end = timer()

            stats.setdefault('num_calls', 0)
            stats['num_calls'] += 1

            stats.setdefault('cum_time', 0.0)
            stats['cum_time'] += end - start

            return res
        return closure
    return closure0

@time_me(time.time, statistic)
def som_func(x, y):
    time.sleep(1.1)

som_func(1, 2)
som_func(1, 2)

assert statistic['num_calls'] == 2
assert 2.5 > statistic['cum_time'] > 2
