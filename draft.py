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
        try:
            return self.__value
        except:
            raise AttributeError("trying to get value of empty field")

    def __set__(self, instance, value):
        if type(value) is self.field_type:
            self.__value = value
        else:
            raise TypeError("incorrent type of value {}: {} expected", type(value), self.field_type)

#class IntField(TypeField):
#    def __init__(self):
#        super(IntField, self).__init__(int)

class MetaField(type):
    def __new__(cls, name, bases, dct):
        new_cls = super(MetaField, cls).__new__(cls, name, bases, dct)
        #new_cls.__value 
        return new_cls

class Class():
    def __init__(self, ftype):
        self.__dict__["ftype"] = ftype

    def my_setattr(self, attr, value):
        print "try to set '%s' to '%s'" % (attr, value)

        if type(value) is self.ftype:
            print "set '%s' to '%s'" % (attr, value)
            self.__dict__[attr] = value
        else:
            raise TypeError("incorrect type {} ({} expected)".format(type(value), ftype))

    x = property(fset=my_setattr)

class IntField(object):
    __metaclass__ = MetaField

class StringField(TypeField):
    def __init__(self):
        super(StringField, self).__init__(str)

class ListField(TypeField):
    def __init__(self):
        super(ListField, self).__init__(list)

class MetaD(type):
    def __new__(cls, name, bases, dct):
        print name
        print bases
        print dct
        #dct['__' + name] = name
        new_cls = super(MetaD, cls).__new__(cls, name, bases, dct)

        #print "===", new_cls.__dict__
        return new_cls

class D(object):
    __metaclass__ = MetaD
    x = IntField()

class C(object):
    x = IntField0('x')
    y = IntField()
    s = StringField()
    lst = ListField()
    z = TypeField(int)

if __name__ == "__main__":
    c = Class(int)
    c.x =  1
    print c.x

    #d = D()
    #d.x = 3

    #dd = D()
    #print dd.x

    #print d.x

    #d.y = 5
    #print d.y
    import sys
    sys.exit(0)
    c = C()
    try:
        c.lst = "abacaba"
        assert False
    except TypeError:
        pass

    c.x = 12
    ok (12) == (c.x)

    try:
        print "c.y - empty:", c.y
        print c.y.__dict__
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

    c1 = C()
    c1.z = 1
    c2 = C()
    c2.z = 2
    print c1.z, c2.z
