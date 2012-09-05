#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import subprocess
import sys


class TCP(object):
    class Rule(object):
        """ for convienient formating """
        def __init__(self, before="", pattern="", after="", objtype=str):
            self.before = before
            self.pattern = pattern
            self.after = after
            self.objtype = objtype

    """ TCP packet """
    __ip_fmt = "\d+\.\d+\.\d+\.\d+"
    __port_fmt = "[0-9]|[1-9]\d*"

    fs = ["time", "protocol", "source_ip", "source_port", "dest_ip", "dest_port", "flags", "seq", "ack", "win", "options",\
        "length"]

    fmt_dict = { \
        "time": Rule("", "\d{2}:\d{2}:\d{2}[.]\d+", "\s"), \
        "protocol": Rule("", "[A-Z]+", "\s"), \
        "source_ip": Rule("", __ip_fmt, "[.]"), \
        "source_port": Rule("", __port_fmt, "\s>\s", int), \
        "dest_ip": Rule("", __ip_fmt, "[.]"), \
        "dest_port": Rule("", __port_fmt, ":\s+", int), \
        "flags": Rule("Flags\s+\[", "[^\s]+", "\],?\s?"), \
        "seq": Rule("", "seq\s\d+:?\d*", "?,?\s?"), \
        "ack": Rule("", "ack\s\d+", "?,?\s?", int), \
        "win": Rule("", "win\s\d+", "?,?\s?", int), \
        "options": Rule("", "options\s\[[^]]+\]", "?,?\s+", list), \
        "length": Rule("", "length\s\d+", "$", int), \
        }

    format_str = "".join([ "%s(%s)%s" % (fmt_dict[f].before, fmt_dict[f].pattern, fmt_dict[f].after) for f in fs])
    
    def __init__(self, datastr):
        def __chop(st):
            if len(st) > 2:
                return st[1:-1].split(',')

        #print "Packet Data:", datastr
        m = re.search(TCP.format_str, datastr)
        if m:
            fields = m.groups()
            for i in range(len(TCP.fs)):
                self.__dict__[TCP.fs[i]] = fields[i]
                prefix = TCP.fs[i] + " "
                if self.__dict__[TCP.fs[i]] != None and self.__dict__[TCP.fs[i]].startswith(prefix):
                    self.__dict__[TCP.fs[i]] = self.__dict__[TCP.fs[i]].replace(prefix, "", 1)
                    if isinstance(TCP.fmt_dict[TCP.fs[i]].objtype(self.__dict__[TCP.fs[i]]), list):
                        self.__dict__[TCP.fs[i]] = __chop(self.__dict__[TCP.fs[i]])
                    else:
                        self.__dict__[TCP.fs[i]] = TCP.fmt_dict[TCP.fs[i]].objtype(self.__dict__[TCP.fs[i]])
        else:
            raise TypeError("can't parse packet data string")

    def __str__(self):
        return "Packet:\n" + "\n".join([ "\t" + str(var) + " = " + str(self.__dict__[var] if self.__dict__[var] != None \
            else str(self.__dict__[var])) for var in TCP.fs])

    def __repr__(self):
        res = "<class TCP " + re.search("at .*", super(TCP, self).__repr__()).group() + "\n"
        res += ("\n".join(["\t" + TCP.fs[i] + ": " + repr(type(self.__dict__[TCP.fs[i]])) for i in range(len(TCP.fs))]))

        return res

def tcpdump(interface, max_count=None):
    """ generator for tcp packets from dev"""
    i = 0
    while 1:
        if max_count != None:
            if i == max_count:
                return
            i += 1

        with open("/dev/null", "w") as dev_null:
            tcpdump_output = subprocess.check_output(["tcpdump", "tcp", "-n", "-c1", "-i" + interface], \
                stderr=dev_null).splitlines()

        if len(tcpdump_output) == 1:
            yield TCP(tcpdump_output[0])
        else:
            raise RuntimeError("tcpdump internal error")

    
if __name__ == "__main__":
    for packet in tcpdump('eth2', 2):
        print packet
        print repr(packet)
        print "Packet dest_ip = ", packet.dest_ip
        print "Packet source_port = ", packet.source_port
