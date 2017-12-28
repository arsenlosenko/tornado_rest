#!/usr/bin/env python3

import os
from tornado.web import RequestHandler, Application
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from utils import psql_connection

PORT = 8899


@psql_connection
def update_books(cur, book, author):
    cur.execute("insert into books (book, author) values ('{}', '{}')".format(book, author))
    cur.execute("insert into prices (book) values ('{}')".format(book))


@psql_connection
def update_prices(cur, book, price):
    cur.execute("insert into prices (book, price) values ('{}', '{}')".format(book, price))


@psql_connection
def get_db_info(cur, table):
    cur.execute("select * from {};".format(table))
    return cur.fetchall()


class MainHandler(RequestHandler):
    def get(self):
        self.render("index.html")


class BooksHandler(RequestHandler):
    def get(self):
        response = self.format_response()
        self.write(response)

    def post(self):
        book = self.get_argument("book")
        author = self.get_argument("author")
        if (book is not None and type(book) == str) \
        and (author is not None and type(author) == str):
            update_books(book, author)
            self.write("info updated")
        else:
            self.write("check the query, arguments 'book' and 'author' should be used as string")

    def format_response(self):
        books = get_db_info("books")
        response = {"info": [],
                    "ref": "/api/v1/books"}
        for book in books:
            response['info'].append({"id": book[0], "book": book[1], "author": book[2]})
        return response


class PricesHandler(RequestHandler):
    def get(self):
        response = self.format_response()
        self.write(response)

    def post(self):
        book = self.get_argument("book")
        price = self.get_argument("price")
        if (book is not None and type(book) == str) \
        and (price is not None and type(price) == str):
            update_prices(book, price)
            self.write("info updated")
        else:
            self.write("check the query, arguments 'book' and 'author' should be used as string")

    def format_response(self):
        prices = get_db_info("prices")
        response = {"prices": [],
                    "ref": "/api/v1/prices"}
        for price in prices:
            response['prices'].append({"id": price[0], "book": price[1], "price": price[2]})
        return response


def main():
    dirname = os.path.dirname(__file__)
    settings = {
        "template_path": os.path.join(dirname, "templates"),
        "static_path": os.path.join(dirname, "static")
    }
    app = Application([
            (r"/", MainHandler),
            (r"/api/v1/books/", BooksHandler),
            (r"/api/v1/prices/", PricesHandler)
        ], **settings)
    http_server = HTTPServer(app)
    http_server.listen(PORT)
    IOLoop.current().start()


if __name__ == "__main__":
    try:
        print("Starting server on port", PORT)
        main()
    except KeyboardInterrupt as e:
        print("Execution stopped")
