#!/usr/bin/env python3

from tornado.web import RequestHandler
from utils import update_books, update_prices, get_db_info


class MainHandler(RequestHandler):
    def get(self):
        self.render("index.html")


class BooksHandler(RequestHandler):
    def get(self):
        response = self.format_response()
        self.write(response)

    def post(self):
        book = self.get_body_argument("book")
        author = self.get_body_argument("author")
        if (book and type(book) == str) \
        and (author and type(author) == str):
            update_books(book, author)
            self.write({"status_code": 201})

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
        book = self.get_body_argument("book")
        price = self.get_body_argument("price")
        if (book and type(book) == str) \
        and (price and type(price) == str):
            update_prices(book, price)
            self.write({"status_code": 201})

    def format_response(self):
        prices = get_db_info("prices")
        response = {"prices": [],
                    "ref": "/api/v1/prices"}
        for price in prices:
            response['prices'].append({"id": price[0], "book": price[1], "price": price[2]})
        return response