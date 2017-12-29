#!/usr/bin/env python3

from models import Book, Price
from gino.ext.tornado import GinoRequestHandler


class MainHandler(GinoRequestHandler):
    def get(self):
        self.render("index.html")


class BooksHandler(GinoRequestHandler):
    async def get(self):
        response = {"info": [],
                    "ref": "/api/v1/books/"}
        books = await Book.query.gino.all()
        for book in books:
            response['info'].append({"id": book.id, "book": book.book, "author": book.author})
        self.write(response)

    async def post(self):
        book = self.get_body_argument("book")
        author = self.get_body_argument("author")
        if book and author:
            await Book.create(book=book, author=author)
            self.write({"status": "added new price",
                        "status_code": 201})


class PricesHandler(GinoRequestHandler):
    async def get(self):
        response = {"info": [],
                    "ref": "/api/v1/prices/"}
        prices = await Price.query.gino.all()
        for price in prices:
            response['info'].append({"id": price.id, "book": price.book, "price": price.price})
        self.write(response)

    async def post(self):
        book = self.get_body_argument("book")
        price = self.get_body_argument("price")
        if book and price:
            await Price.create(book=book, price=price)
            self.write({"status": "added new price",
                        "status_code": 201})

