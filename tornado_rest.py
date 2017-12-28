#!/usr/bin/env python3

import logging
from tornado.web import RequestHandler, Application
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from utils import psql_connection

PORT = 8899


@psql_connection
def update_books(cur, book, author):
    cur.execute("insert into books (book, author) values ('{}', '{}')".format(book, author))


@psql_connection
def get_books(cur):
    cur.execute("select * from books;")
    return cur.fetchall()


class MainHandler(RequestHandler):
    def get(self):
        self.render("api.html")


class BooksHandler(RequestHandler):
    def get(self):
        response = self.format_response()
        self.write(response)

    def post(self):
        book = self.get_argument("book")
        author = self.get_argument("author")
        update_books(book, author)
        self.write("info updated")

    def format_response(self):
        books = get_books()
        response = {"info": [],
                    "ref": "/api/v1/books"}
        for book in books:
            response['info'].append({"id": book[0], "book": book[1], "author": book[2]})
        return response


def main():
    app = Application([
            (r"/", MainHandler),
            (r"/api/v1/books/", BooksHandler)
        ])
    http_server = HTTPServer(app)
    http_server.listen(PORT)
    IOLoop.current().start()


if __name__ == "__main__":
    try:
        print("Starting server on port", PORT)
        main()
    except KeyboardInterrupt as e:
        print("Execution stopped")
