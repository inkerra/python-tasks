#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
#from importlib import import_module
#import glob
import imp
import inspect
import re

DEBUG_MODE = 1

def dbg(msg):
    if DEBUG_MODE: sys.stderr.write(msg + "\n")

def source_file(f):
    if f.rfind('.') == -1: return f
    return f[:- len(f) + f.rfind('.')] + '.py'

def import_module_by_path(filepath):
    mod_name, file_ext = os.path.splitext(os.path.split(filepath)[-1])
    if file_ext == ".py":
        dbg("importing {} from {}".format(mod_name, filepath))
        if sys.modules.has_key(mod_name): del sys.modules[mod_name]
        try:
            return imp.load_source(mod_name, filepath)
        except:
            pass
    elif re.match("\.py[ocd]|\.so", file_ext):
        if os.path.exists(source_file(filepath)):
            dbg("skipped (source file exists) {} from {}".format(mod_name, filepath))
            return

        if sys.modules.has_key(mod_name): del sys.modules[mod_name]
        dbg("importing (compiled) {} from {}".format(mod_name, filepath))
        try:
            return imp.load_compiled(mod_name, filepath)
        except:
            pass
    else:
        return
    dbg("skipped (can't load) {}".format(filepath))

def aspect_python(directory, regexp):
    for (path, dirs, files) in os.walk(directory):
        for f in files:
            mod_obj = import_module_by_path(os.path.join(path, f))
            if mod_obj:
                for elem in dir (mod_obj):
                    obj = getattr(mod_obj, elem)
                    if  inspect.isclass(obj) and re.match(regexp, obj.__name__):
                        yield obj

__all__ = ['aspect_python']

if __name__ == "__main__":
    for d in aspect_python("plugins", r'D\d\d\d'):
        print "D\d\d\d:", d()
    for cls in aspect_python("plugins", r'MyNewO.*'):
        cls().action(2)
    for cls in aspect_python("plugins", r'MyNewA.*'):
        cls().action()
    for d in aspect_python("plugins", r'D1\d\d'): print "D1\d\d:", d()
