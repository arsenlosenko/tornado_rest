#!/usr/bin/env python3

from tornado.log import LogFormatter
from tornado.web import Application
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import options, define, parse_config_file
from handlers import MainHandler, BooksHandler, PricesHandler


def main():
    LogFormatter()
    define("port", type=int)
    define("settings", type=dict)
    parse_config_file("config.py")
    routes = [
            (r"/", MainHandler),
            (r"/api/v1/books/", BooksHandler),
            (r"/api/v1/prices/", PricesHandler)
        ]
    settings = options.settings
    http_server = HTTPServer(Application(routes, **settings))
    http_server.listen(options.port)
    print("Starting server on port {} (Ctrl-C to stop the server)".format(options.port))
    IOLoop.current().start()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt as e:
        print("Execution stopped")
