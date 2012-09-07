#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import sys

host = 'localhost'
port = 5000
backlog = 5
size = 1024

while 1:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host,port))
    s.listen(backlog)
    
    sock, address = s.accept()
    
    print "server: got connection from %s port %d\n" % (address[0], address[1])
    sock.send("Welcome to server\n")

    while 1:
        data = sock.recv(size)
        if len(data) == 0:
            sock.send("buy")
            break
        else:
            sock.send(data)
            print "RECV: %d bytes\n" % len(data)
    
    sock.close()
