#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from nose.tools import eq_

import sys
sys.path.insert(0, "../")
from serialization.serialize import serialize
from serialization.deserialize import deserialize
from serialization.common import SerializationError

class IntTestCase(unittest.TestCase):
    def test_boundaries(self):
        eq_(0, deserialize(serialize(0)))
        eq_(-sys.maxint - 1, deserialize(serialize(-sys.maxint - 1)))
        eq_(sys.maxint, deserialize(serialize(sys.maxint)))

class StringTestCase(unittest.TestCase):
    def test_empty(self):
        eq_("", deserialize(serialize("")))

    def test_one_char(self):
        eq_('c', deserialize(serialize('c')))

    def test_str(self):
        for _ in {"ab", "aba", "]ab", ">a", "<b", "a>", "b]"}:
            eq_(_, deserialize(serialize(_)))
                    
class ListEmptyTestCase(unittest.TestCase):
    def test_empty(self):
        eq_([], deserialize(serialize([])))

class IntOneElementListTestCase(unittest.TestCase):
    def test_one_digit_element(self):
        eq_([0], deserialize(serialize([0])))

    def test_not_one_digit_element(self):
        eq_([10], deserialize(serialize([10])))

class IntListSomeElements(unittest.TestCase):
    def test_int_list_elements(self):
        lst = [1, [], 12]
        eq_(lst, deserialize(serialize(lst)))

class ListOfListSomeElements(unittest.TestCase):
    def test_empty(self):
        lst = []
        for depth in range(0, 3):
            eq_(lst, deserialize(serialize(lst)))
            lst = [lst]
        eq_([1], deserialize(serialize([1])))

class ExceptionsTestCase(unittest.TestCase):
    def test_nonsupported_type(self):
        try:
            serialize(1.2)
        except:
            assert True

        try:
            deserialize('<int>')
        except:
            assert True

        try:
            deserialize('<int=')
        except:
            assert True

        try:
            deserialize('<aba=caba>')
        except:
            assert True
        
        try:
            deserialize('[<int=0>]<int=1>')
        except:
            assert True
        
        try:
            deserialize('[>]')
        except:
            assert True
        try:
            deserialize('~')
        except:
            assert True
