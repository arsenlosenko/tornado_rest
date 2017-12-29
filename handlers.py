#!/usr/bin/env python3

from tornado.web import RequestHandler
from utils import DBConnect


class MainHandler(RequestHandler):
    def get(self):
        self.render("index.html")


class BooksHandler(RequestHandler, DBConnect):
    def get(self):
        response = self.format_response()
        self.write(response)

    def post(self):
        book = self.get_body_argument("book")
        author = self.get_body_argument("author")
        if book and author:
            self.insert_book(book, author)
            self.write({"status": "added new price",
                        "status_code": 201})

    def format_response(self):
        books = self.get_db_info("books")
        response = {"info": [],
                    "ref": "/api/v1/books"}
        for book in books:
            response['info'].append({"id": book[0], "book": book[1], "author": book[2]})
        return response


class PricesHandler(RequestHandler, DBConnect):
    def get(self):
        response = self.format_response()
        self.write(response)

    def post(self):
        book = self.get_body_argument("book")
        price = self.get_body_argument("price")
        if book and price:
            self.insert_price(book, price)
            self.write({"status": "added new price",
                        "status_code": 201})

    def format_response(self):
        prices = self.get_db_info("prices")
        response = {"prices": [],
                    "ref": "/api/v1/prices"}
        for price in prices:
            response['prices'].append({"id": price[0], "book": price[1], "price": price[2]})
        return response