#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
#import sys
#from importlib import import_module
#import glob
import imp
import inspect
import re

def import_module_by_path(filepath):
    mod_name, file_ext = os.path.splitext(os.path.split(filepath)[-1])
    try:
        if file_ext == "py":
            return imp.load_source(mod_name, filepath)
        elif re.match("py[ocd]|so", file_ext):
            return imp.load_compiled(mod_name, filepath)
    except:
        print "Skipped {}".format(filepath)

def aspect_python(directory, regexp):
    for (path, dirs, files) in os.walk(directory):
        for f in files:
            mod_obj = import_module_by_path(os.path.join(path, f))
            if mod_obj:
                for elem in dir (mod_obj):
                    obj = getattr(mod_obj, elem)
                    if  inspect.isclass(obj) and re.match(regexp, obj.__name__):
                        yield obj

if __name__ == "__main__":
    for d in aspect_python("plugins", r'D\d\d\d'):
        print "aspect:", d()
    for cls in aspect_python("plugins", r'MyNewO.*'):
        cls().action(2)
