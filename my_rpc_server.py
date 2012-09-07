#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import struct
import binascii

class RPCServer:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.funcs = {}

    def register_function(self, function, name=None):
        if name is None:
            name = function.__name__
        self.funcs[name] = function

    def call(self, name, *params):
        return self.funcs[name](*params)

    def run(self):
        while 1:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((self.ip, self.port))
            s.listen(5)
            
            conn, address = s.accept()
            
            try:
                while 1:
                    unpacker_fmt = conn.recv(1024)

                    unpacker = struct.Struct(unpacker_fmt)

                    data = conn.recv(unpacker.size)

                    if len(data) == 0:
                        break
                    else:
                        req = unpacker.unpack(data)
                        #print ("NAME: " + str(req[0]) + "\n")
                        params = req[1:]
                        #for p in params:
                        #    print ("param: " + str(p) + "\n")
                        res = self.call(req[0], *req[1:])
                        conn.sendall(str(res))
            except:
                raise
            finally:
                conn.close()

if __name__ == "__main__":
    def func1(x, a, b, c):
        return a * x ** 2 + b * x + c
        
    srv = RPCServer("localhost", 8000)
    srv.register_function(lambda x, y: x + y, "add")
    srv.register_function(lambda x: x, "same")
    srv.register_function(func1)
    srv.run()
