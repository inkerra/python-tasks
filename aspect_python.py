#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
#import sys
#from importlib import import_module
#import glob
import imp
import inspect
import re

def aspect_python(directory, regexp):
    res = []
    for (path, dirs, files) in os.walk(directory):
        for f in files:
            if f.endswith(".py"):
                filepath = os.path.join(path, f) 
                mod_name, file_ext = os.path.splitext(os.path.split(filepath)[-1])
                try:
                    mod_obj = imp.load_source(mod_name, filepath)
                except:
                    print "Warning: can't load {} from {}, skipped".format(mod_name, filepath)
                    continue

                for elem in dir (mod_obj):
                    obj = getattr(mod_obj, elem)
                    if  inspect.isclass(obj) and re.match(regexp, obj.__name__):
                            res.append(obj)
    return res
if __name__ == "__main__":
    for d in aspect_python("plugins", r'D\d\d\d'):
        print "aspect:", d()
    for cls in aspect_python("plugins", r'MyNewO.*'):
        cls().action(2)
