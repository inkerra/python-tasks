#!/usr/bin/env python
# -*- coding: utf-8 -*-

LF, RG = range(2)

def get_code(c):
    i, res = 0, 0
    while c != None:
        if parent[c][0] != None:
            if parent[c][0]: 
                res |= 1 << i
        c = parent[c][1]
        i += 1
    return res

with open("file", "rb") as fd:
    content = fd.read()

occur_table = {}
for byte in content:
    occur_table.setdefault(byte, 0)
    occur_table[byte] += 1

free_nodes = [ (x[1], x[0]) for x in occur_table.items()]

parent = {}
while len(free_nodes) > 1:
    free_nodes.sort()
    lf = free_nodes[0]
    rg = free_nodes[1]

    del free_nodes[1]
    del free_nodes[0]

    new_node = (lf[0] + rg[0], lf[1] + rg[1])

    parent[lf[1]] = (LF, new_node[1])
    parent[rg[1]] = (RG, new_node[1])

    free_nodes.append(new_node)

root = free_nodes[0][1]
parent[root] = (None, None)

code = {}
for leaf in occur_table.keys():
    code[leaf] = get_code(leaf)

with open("code.pkl", "wb") as fd:
    import pickle
    pickle.dump(code, fd)

with open("new_file", "wb") as fd:
    import struct
    for byte in content:
        fd.write(struct.pack('b', code[byte]))
