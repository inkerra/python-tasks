#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import glob
import sys
from importlib import import_module
import imp
from opt_plugin.plugin import MetaOpt, Opt

def update(d, from_class_dict,  name_in_dict, name):
    val = from_class_dict.__dict__.get(name, None)
    if val is None: return
    d[name_in_dict] = val

def import_plugins(directory):
    for (path, dirs, files) in os.walk(directory):
        for f in files:
            if f.endswith(".py"):
                name = f[:-3]
                if sys.modules.has_key(name):
                    old = sys.modules[name].__file__
                    if old.endswith(".pyc") or old.endswith(".pyo"):
                        old = old[:-1]
                    modfile = os.path.join(path, f)
                    if old != modfile:
                        print "Warning: the same module name for {} and {}".format(modfile, old)
                        del sys.modules[name]
                saved_sys_path = sys.path
                sys.path.insert(0, path)
                sys.modules[name] = import_module(name)
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
    import_plugins("plugins")
    set_options()
