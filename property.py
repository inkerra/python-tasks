#!/usr/bin/env python
# -*- coding: utf-8 -*-

from oktest import ok

class IntField0(object): # requires name parameter
    def __init__(self, name):
        self.__name = name

    def __get__(self, instance, value):
        if not instance.__dict__.has_key(self.__name):
            raise AttributeError("trying to get value of empty field")
        return instance.__dict__[self.__name]

    def __set__(self, instance, value):
        if type(value) is int:
            instance.__dict__[self.__name] = value
        else:
            raise TypeError("incorrect type of value")

class TypedField(object):
    typed = None

class IntField(TypedField):
    typed = int

class StringField(TypedField):
    typed = str

class ListField(TypedField):
    typed = list

class MetaD(type):
    def __new__(cls, name, bases, dct):
        for key, val in dct.items():
            if isinstance(val, TypedField):
                def setter(key, vtype):
                    def closure(instance, value):
                        if type(value) is vtype:
                            instance.__dict__[key] = value
                        else:
                            raise TypeError("incorrect type")
                    return closure
                def getter(key):
                    def closure(instance):
                        if instance.__dict__.has_key(key):
                            return instance.__dict__[key]
                        else:
                            raise AttributeError("empty property")
                    return closure
                if val.__class__.typed is None:
                    raise TypeError("type is not set")
                dct[key] = property(getter(key), setter(key, val.__class__.typed))
        return super(MetaD, cls).__new__(cls, name, bases, dct)

class D(object):
    __metaclass__ = MetaD

class C(D):
    x = IntField()
    s = StringField()
    lst = ListField()
    z = IntField()

if __name__ == "__main__":
    c = C()
    try:
        c.x
        assert False
    except:
        pass
    c.x = 1
    ok (c.x) ==  (1)
    c.x = 2
    ok (c.x) ==  (2)
    try:
        c.x = 's'
        assert False
    except:
        pass
    c.z = 100
    assert c.z == 100
    ok (c.x) == (2)

    c = C()
    try:
        c.lst = "abacaba"
        assert False
    except TypeError:
        pass

    c.x = 12
    ok (12) == (c.x)

    try:
        c.y
        assert False
    except AttributeError:
        pass

    c.y = 13
    ok (25) == (c.x + c.y)
    c.y = "abacaba" # y - is not fixed typed
    ok (c.y) == "abacaba"

    try:
        c.s
        assert False
    except AttributeError:
        pass

    try:
        c.s = 12
        assert False
    except TypeError:
        pass

    c.s = "abacaba"
    ok ("abacaba") == (c.s)

    try:
        print c.lst
        assert False
    except AttributeError:
        pass

    try:
        c.s = 12
        assert False
    except TypeError:
        pass

    try:
        c.lst = "abacaba"
        assert False
    except TypeError:
        pass

    c.lst = [c.x, c.y, c.s]
    ok ([c.x, c.y, c.s]) == c.lst

    c1 = C()
    c1.z = 1
    c2 = C()
    c2.z = 2
    assert c1.z != c2.z
