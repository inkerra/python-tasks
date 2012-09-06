#!/usr/bin/env python
#-*- coding: utf-8 -*-

import urllib2
import Queue
import threading
import socket
socket.setdefaulttimeout(5)

def __get_content(url):
    try:
        return urllib2.urlopen(url).read()
    except Exception as e:
        return None
    
def __loader(param_q, res_q, func):
    while 1:
        param = param_q.get()
        if param is None: break
        res_q.put((param, func(param)))

def load_pages(max_thread_pool_sz, *urls):
    """ generator of loaded pages """
    param_q = Queue.Queue()
    res_q = Queue.Queue()

    loader_params = (param_q, res_q, __get_content)
    loaders = []

    for u in urls:
        param_q.put(u)

    for i in range(max_thread_pool_sz):
        param_q.put(None)

    for i in range(max_thread_pool_sz):
        th = threading.Thread(None, __loader, "loader-{}".format(i), loader_params)
        th.daemon = True
        th.start()
        loaders.append(th)

    for url in urls:
        content = res_q.get()
        yield content

    for th in loaders:
        th.join()

if __name__ == "__main__":
    urls = [ \
    "https://google.com", \
    "http://localhost", \
    "http://inkerrapp.appspot.com/?act=show&key=agtzfmlua2VycmFwcHImCxIEQmxvZyIMZGVmYXVsdF9ibG9nDAsSCEJsb2dQb3N0GLHqAQw",
    "http://inkerrapp.appspot.com/?act=show&key=agtzfmlua2VycmFwcHIlCxIEQmxvZyIMZGVmYXVsdF9ibG9nDAsSCEJsb2dQb3N0GPIuDA",
    "incorrect_url",
    ]

    for url, page in load_pages(2, *urls):
        if page is not None:
            print url, len(page)
        else:
            print "ERROR: can't open {}".format(url)
