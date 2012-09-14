#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web
import tornado.httpserver
import tornado.ioloop
import os

import pymongo
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017

import tornado.options
from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', RootHandler),
        ]

        settings = dict(
            template_path = os.path.join(os.path.dirname(__file__), "templates"),
            static_path = os.path.join(os.path.dirname(__file__), "static"),
        )

        tornado.web.Application.__init__(self, handlers, **settings)

        self.connection = pymongo.Connection(MONGODB_HOST, MONGODB_PORT)
        self.db = self.connection['tornado']

class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

class RootHandler(BaseHandler):
    def get(self):
        self.write("Hello, world!")

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
