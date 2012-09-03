#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pickle
import struct
import cPickle
import array
import marshal

LF, RG = range(2)
MAX_BITS = 8

# node in Huffman tree
class Node(object):
    def __init__(self, byte=None, w=None, lnode=None, rnode=None, parent=None):
        self.LF = lnode
        self.RG = rnode
        self.parent = parent
        self.byte = byte
        self.w = w # weight

    def __cmp__(self, other): # comparator for sorting by weight
        if not isinstance(other, Node):
            return super(Node, self).__cmp__(other)
        return cmp(self.w, other.w)

# builds Huffman tree
def build_tree(nodes):
    while 1:
        nodes.sort()
        if len(nodes) < 2:
            return nodes[0]

        fst = nodes[0]
        snd = nodes[1]
        del nodes[0]
        del nodes[0]
        parent = Node(lnode=fst, rnode=snd, w = fst.w + snd.w)
        fst.parent = parent
        snd.parent = parent

        nodes.append(parent)

# generates Huffman code
def gen_code(node, code_map, buff_stack=[]):
    if not node.LF and not node.RG:
        code_map[node.byte] = ''.join(buff_stack)
        return

    buff_stack.append('0')
    gen_code(node.LF, code_map, buff_stack)
    buff_stack.pop()

    buff_stack.append('1')
    gen_code(node.RG, code_map, buff_stack)
    buff_stack.pop()

# decodes Huffman code
def decode(root, code_len, array_codes):
    buf = []
    total_len = 0
    node = root

    for code in array_codes:
        buf_len = 0
        while (buf_len < MAX_BITS and total_len < code_len):
            buf_len += 1
            total_len += 1

            if code >> (MAX_BITS - buf_len) & 1:
                node = node.RG
                if node.byte:
                    buf.append(node.byte)
                    node = root
            else:
                node = node.LF
                if node.byte:
                    buf.append(node.byte)
                    node = root
    return ''.join(buf)

if __name__ == "__main__":
    origin_file = "origin.file"
    compressed_file = "compressed.file"
    decompressed_file = "decompressed.file"
    
    # encoding
    with open(origin_file, "rb") as fd:
        content = fd.read()

    occur_table = {}
    for byte in content:
        occur_table.setdefault(byte, 1)
        occur_table[byte] += 1

    root = build_tree([Node(byte = byte, w = int(w)) for (byte, w) in occur_table.iteritems()])

    code_map = {}
    gen_code(root, code_map)

    array_codes = array.array('B')
    code_length = 0
    buff, buf_len = 0, 0
    for byte in content:
        code = code_map[byte]
        for bit in list(code):
            if bit == '1':
                buff = (buff << 1) | 1
            else:
                buff = (buff << 1)
            buf_len += 1
            if buf_len == MAX_BITS:
                array_codes.extend([buff])
                buff, buf_len = 0, 0
        code_length += len(code)

    if buf_len != 0:
        array_codes.extend([buff << (MAX_BITS - buf_len)])

    with open(compressed_file, "wb") as fd:
        marshal.dump((cPickle.dumps(root), code_length, array_codes), fd)

    # decoding
    with open(compressed_file, "rb") as fd:
        unpickled_root, length, array_codes = marshal.load(fd)
    
    root = cPickle.loads(unpickled_root)
    array_codes = array.array('B', array_codes)

    decoded = decode(root, length, array_codes)

    with open(decompressed_file, "wb") as fd:
        fd.write(decoded)
