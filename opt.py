#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

class MetaOpt(type):
    all_data = []
    def __new__(cls, name, bases, dct):
        for i in dct.items():
            if i[0] == 'opt':
                opt = i[1]
            if i[0] == 'action':
                action = i[1]
        if opt is None or action is None:
            opt, action = '', '' # interface
        MetaOpt.all_data.append((opt, action))
        return super(MetaOpt, cls).__new__(cls, name, bases, dct)

class Opt(object):
    __metaclass__ = MetaOpt

    @classmethod
    def action(cls):
        pass
    opt = ''

class MyNewAction(Opt):
    @classmethod
    def action(cls):
        print "My new action"

    opt = '--act'

def main():
    parser = argparse.ArgumentParser()
    for opt, action in MetaOpt.all_data[1:]:
        parser.add_argument(opt, action="store_true")

    options = vars(parser.parse_args())
    for option, value in options.items():
        print "option:{} value:{}".format(option, value)
        if option:
            print value
        else:
            print "no " + option
    #MyNewAction().action()


    
if __name__ == "__main__":
    main()
