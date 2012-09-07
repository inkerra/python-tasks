#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
socket.setdefaulttimeout(5)
import struct
import binascii
import array
import ctypes

class RPCClient:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def __getattr__(self, name):
        def cb(*args):
            packer_fmt = []
            nargs = [name] + list(args)
            for a in nargs:
                if isinstance(a, int):
                    packer_fmt.append('i')
                elif isinstance(a, str):
                    packer_fmt.append(str(len(a)) + 's')
                else:
                    # list ???
                    pass

            packer_fmt = " ".join(packer_fmt)

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.connect((self.ip, self.port))

            try:
                s.sendall(packer_fmt)

                packer = struct.Struct(packer_fmt)
                values = nargs
                #print "values:", values
                packed_data = packer.pack(*values)

                s.sendall(packed_data)

                resp = s.recv(1024)
                print resp
            finally:
                s.close()
        return cb


if __name__ == "__main__":
    c = RPCClient("localhost", 8000)
    c.same(1)
    c.add(1, 2)
    c.func1(2, 1, 2, 3)
