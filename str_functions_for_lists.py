#! /usr/bin/env python
# -*- coding: utf-8 -*-

def replace(str1, str2, str3):
    res = str1

    if str2 == str3:
        return res

    while 1:
        ndx = res.find(str2)
        if ndx == -1:
            return res
        res =  res[:ndx] + str3 + res[ndx + len(str2):]

def split(str1, str2):
    if str2 == "":
        raise ValueError("empty separator")

    if str1 == "":
        return ['']

    res = []
    while 1:
        ndx = str1.find(str2)
        if ndx == -1:
            if len(str1): res += [str1]
            return res
        res += [str1[:ndx]]
        str1 = str1[ndx + len(str2):]
        if len(str1) == 0:
            res += ['']

def join(str1, array):
    if array == []:
        return ""

    res = array[0]
    for s in array[1:]:
        res += str1 + s
    return res

def capitalize(str1):
    if 'a' <= str1[0] <= 'z':
        return chr(ord(str1[0]) - ord('a') + ord('A')) + str1[1:]
    return str1

# examples
if __name__ == "__main__":
    assert "t = y" == replace("x = y", "x", "t")
    assert "expr: z != y" == replace("expr: x = y", "x =", "z !=")
    assert "zz == zz" == replace("x == x", "x", "zz")
    
    assert "a + ba + caba" == join(" + ", ["a", "ba", "caba"])
    assert "a" == join(" + ", ["a"])
    assert "" == join(" + ", [])
    
    assert ['', 'b', 'c', 'b', ''] == split("abacaba", "a")
    assert ['a', ' ba', ' caba'] == split("a, ba, caba", ",")
    assert [''] == split("", ",")
    try:
        print split("abacaba", "")
        assert False
    except ValueError, e:
        assert "ValueError captured: empty separator" == "ValueError captured: %s" % e
    
    assert "Str" == capitalize("str")
    assert "=str" == capitalize("=str")
