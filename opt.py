#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import subprocess
import sys

class MetaOpt(type):
    all_data = []
    def __new__(cls, name, bases, dct):
        is_interface = False
        for i in dct.items():
            if i[0] == 'opt':
                opt = i[1]
        new_cls = super(MetaOpt, cls).__new__(cls, name, bases, dct)
        if not is_interface:
            MetaOpt.all_data.append((opt, new_cls))
        return new_cls

class Opt(object):
    """ interface for Action classes """
    __metaclass__ = MetaOpt

    @classmethod
    def action(cls, *vals):
        pass
    opt = '--act'

def update(d, from_class_dict,  name_in_dict, name):
    val = from_class_dict.__dict__.get(name, None)
    if val is None: return
    d[name_in_dict] = val

def import_plugins(directory):
    saved_sys_path = sys.path
    sys.path.insert(0, directory)

    try:
        find_output = subprocess.check_output(["find", directory, \
            "-name", "*.py"]).splitlines()
        for mod in find_output:
            execfile(mod)
    except:
        raise
    finally:
        sys.path = saved_sys_path

def set_options():
    parser = argparse.ArgumentParser()
    d = dict(MetaOpt.all_data)
    for opt, action in d.items():
        kwargs = {}
        update(kwargs, d[opt], 'type', 'value_type')
        update(kwargs, d[opt], 'default', 'default_value')
        update(kwargs, d[opt], 'action', 'action_type')

        if kwargs.has_key('type'):
            kwargs.setdefault('action', 'store')
            parser.add_argument(opt, **kwargs)
        else:
            parser.add_argument(opt, action="store_false")

    options = vars(parser.parse_args())
    for option, value in options.items():
        action = d['--' + option].action
        if action.im_func.func_code.co_argcount == 2: #one without cls
            action(value)
        else:
            action()

if __name__ == "__main__":
    import_plugins("./plugins")
    set_options()
