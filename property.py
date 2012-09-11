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

class TypeField(object):
    def __init__(self, field_type):
        self.field_type = field_type

    def __get__(self, instance, value):
        if not self.__dict__.has_key("__value"):
            raise AttributeError("trying to get value of empty field")
        return self.__dict__["__value"]

    def __set__(self, instance, value):
        if type(value) is self.field_type:
            self.__dict__["__value"] = value
        else:
            raise TypeError("incorrent type of value {}: {} expected", type(value), self.field_type)

class IntField(TypeField):
    def __init__(self):
        super(IntField, self).__init__(int)

class StringField(TypeField):
    def __init__(self):
        super(StringField, self).__init__(str)

class ListField(TypeField):
    def __init__(self):
        super(ListField, self).__init__(list)

class C(object):
    x = IntField0('x')
    y = IntField()
    s = StringField()
    lst = ListField()

if __name__ == "__main__":
    c = C()
    try:
        c.lst = "abacaba"
        assert False
    except TypeError:
        pass

    c.x = 12
    ok (12) == (c.x)
    try:
        print c.y
        assert False
    except AttributeError:
        pass

    c.y = 13
    ok (25) == (c.x + c.y)

    try:
        print c.s
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
        print type(c.lst)
        assert False
    except TypeError:
        pass

    c.lst = [c.x, c.y, c.s]
    ok ([c.x, c.y, c.s]) == c.lst
