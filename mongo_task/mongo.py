#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pymongo import Connection
import xml.etree.ElementTree as ET
import hotshot

prof_files = ["my", "db_conn", "xml", "db"]
profs = {}
for f in prof_files:
    profs[f] = hotshot.Profile(f + '.prof')

profs["my"].start()
host= 'localhost'
port = 27017
db_name = 'test'
user = 'inkerra'
pwd = 'inke123'
profs["my"].stop()

profs["db_conn"].start()
connection = Connection(host, port, safe=True)
db = connection[db_name]
db.authenticate(user, pwd)
profs["db_conn"].stop()

profs["xml"].start()
tree = ET.parse('mongo.xml')
root = tree.getroot()
profs["xml"].stop()

profs["db"].start()
coll = db[root.tag]

for i in root:
    if i.tag == 'pair':
        doc = {i.attrib['key']: i.text}
        try:
            coll.insert(doc, safe=True)
        except:
            print "can't insert {}".format(doc)
#coll.remove()
profs["db"].stop()

for prof in profs.values():
    prof.close()
#for entry in coll.find():
#    print entry
#import IPython
#IPython.embed()
