#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
from StringIO import StringIO

root = ET.Element("data")
for _ in range(100 * 1000):
    pair = ET.SubElement(root, "pair")
    pair.attrib = {'key' : 'some_key%d' % (_ + 1)}
    pair.text = 'some_val%d' % (_ + 1) 

tree = ET.ElementTree(root)
tree.write('mongo.xml', encoding='UTF-8', xml_declaration=True)
