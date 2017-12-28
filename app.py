#!/usr/bin/env python3

import os
from tornado.web import Application
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import options, define
from handlers import MainHandler, BooksHandler, PricesHandler

define("port", default=8899)
define("host", default="localhost")

def main():

    dirname = os.path.dirname(__file__)
    settings = {
        "template_path": os.path.join(dirname, "templates"),
        "static_path": os.path.join(dirname, "static"),
        "autoreload": True
    }
    app = Application([
            (r"/", MainHandler),
            (r"/api/v1/books/", BooksHandler),
            (r"/api/v1/prices/", PricesHandler)
        ], **settings)
    http_server = HTTPServer(app)
    http_server.listen(options.port)
    IOLoop.current().start()


if __name__ == "__main__":
    try:
        print("Starting server on port", options.port)
        main()
    except KeyboardInterrupt as e:
        print("Execution stopped")
