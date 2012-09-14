#!/usr/bin/env python
# -*- coding: utf-8 -*-

import array
import pickle
import cPickle

MAX_BITS_NUM = 8

class Node(object):
    """ node in Huffman tree """
    def __init__(self, lnode=None, rnode=None, parent=None, byte=None, w=None):
        self.left = lnode
        self.right = rnode
        self.parent = parent
        self.byte = byte
        self.w = w # weight

def build_tree(nodes):
    """ builds Huffman tree """
    while 1:
        nodes.sort(key = lambda x: x.w)
        if len(nodes) < 2:
            return nodes[0]

        fst = nodes[0]
        snd = nodes[1]

	nodes = nodes[2:]
	
        parent = Node(lnode = fst, rnode = snd, w = fst.w + snd.w)
        fst.parent = parent
        snd.parent = parent

        nodes.append(parent)

def gen_code(node, code_map, buff_stack=[]):
    """ generates Huffman code """
    if not node.left and not node.right:
        code_map[node.byte] = ''.join(buff_stack)
        return

    buff_stack.append('0')
    gen_code(node.left, code_map, buff_stack)
    buff_stack.pop()

    buff_stack.append('1')
    gen_code(node.right, code_map, buff_stack)
    buff_stack.pop()

def encode(content):
    occur_table = {}
    for byte in content:
        occur_table.setdefault(byte, 0)
        occur_table[byte] += 1

    root = build_tree([Node(byte = byte, w = int(w)) for (byte, w) in occur_table.iteritems()])

    code_map = {}
    gen_code(root, code_map)

    array_codes = array.array('B')
    code_len, buff, buf_len = 0, 0, 0
    for byte in content:
        code = code_map[byte]
        for bit in map(int, list(code)):
            buff = (buff << 1) | bit
            buf_len += 1
            if buf_len == MAX_BITS_NUM:
                array_codes.extend([buff])
                buff, buf_len = 0, 0
        code_len += len(code)

    if buf_len != 0:
        array_codes.extend([buff << (MAX_BITS_NUM - buf_len)])

    return root, code_len, array_codes

def decode(root, code_len, array_codes):
    buf = []
    total_len = 0
    node = root

    for code in array_codes:
        buf_len = 0
        while (buf_len < MAX_BITS_NUM and total_len < code_len):
            buf_len += 1
            total_len += 1

            if code >> (MAX_BITS_NUM - buf_len) & 1:
                node = node.right
                if node.byte:
                    buf.append(node.byte)
                    node = root
            else:
                node = node.left
                if node.byte:
                    buf.append(node.byte)
                    node = root
    return ''.join(buf)

def encode_file(origin_file, compressed_file):
    with open(origin_file, "rb") as fd:
        content = fd.read()

    root, code_len, array_codes = encode(content)

    with open(compressed_file, "wb") as fd:
        pickle.dump((cPickle.dumps(root), code_len, array_codes), fd)

def decode_file(compressed_file, decompressed_file):
    with open(compressed_file, "rb") as fd:
        unpickled_root, length, array_codes = pickle.load(fd)
    
    root = cPickle.loads(unpickled_root)
    array_codes = array.array('B', array_codes)

    decoded = decode(root, length, array_codes)

    with open(decompressed_file, "wb") as fd:
        fd.write(decoded)

if __name__ == "__main__":
    encode_file("origin.file", "compressed.file")
    decode_file("compressed.file", "decompressed.file")
