from tornado.ioloop import IOLoop
from tornado.log import LogFormatter
from tornado.options import options, define, parse_config_file
from gino.ext.tornado import Application
from models import db
from handlers import MainHandler, BooksHandler, PricesHandler, SocketHandler, MessagesHandler


def main():
    LogFormatter()

    define("port", type=int)
    define("settings", type=dict)
    parse_config_file("config.py")

    routes = [
            (r"/", MainHandler),
            (r"/api/v1/books/", BooksHandler),
            (r"/api/v1/prices/", PricesHandler),
            (r"/api/v1/messages/", MessagesHandler),
            (r"/websocket", SocketHandler)
        ]
    settings = options.settings

    IOLoop.configure('tornado.platform.asyncio.AsyncIOMainLoop')
    app = Application(routes, **settings)
    app.listen(options.port)

    print(f"Starting server on port {options.port} (Ctrl-C to stop the server)")
    loop = IOLoop.current().asyncio_loop
    loop.run_until_complete(app.late_init(db))
    loop.run_forever()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt as e:
        print("Execution stopped")
