from tornado.websocket import WebSocketHandler
from gino.ext.tornado import GinoRequestHandler
from models import Book, Price, Message


class BaseHandler(object):
    def __init__(self):
        self.response = {"info": [], "ref": ""}


class MainHandler(GinoRequestHandler):
    def get(self):
        self.render("index.html")


class BooksHandler(GinoRequestHandler, BaseHandler):
    async def get(self):
        entrypoint = '/api/v1/books/'
        books = await Book.query.gino.all()
        for book in books:
            self.response['info'].append({"id": book.id, "book": book.book, "author": book.author})
            self.response['ref'] = entrypoint
        self.write(self.response)

    async def post(self):
        book = self.get_body_argument("book")
        author = self.get_body_argument("author")
        if book and author:
            await Book.create(book=book, author=author)
            self.write({"status": "added new price",
                        "status_code": 201})


class PricesHandler(GinoRequestHandler, BaseHandler):
    async def get(self):
        entrypoint = '/api/v1/prices/'
        prices = await Price.query.gino.all()
        for price in prices:
            self.response['info'].append({"id": price.id, "book": price.book, "price": price.price})
            self.response['ref'] = entrypoint
        self.write(self.response)

    async def post(self):
        book = self.get_body_argument("book")
        price = self.get_body_argument("price")
        if book and price:
            await Price.create(book=book, price=price)
            self.write({"status": "added new price",
                        "status_code": 201})


class MessagesHandler(GinoRequestHandler, BaseHandler):
    async def get(self):
        entrypoint = '/api/v1/messages/'
        messages = await Message.query.gino.all()
        for message in messages:
            self.response['info'].append({"id": message.id, "text": message.text,"date": str(message.date)})
            self.response['ref'] = entrypoint
        self.write(self.response)


class SocketHandler(WebSocketHandler):
    def open(self):
        print("WebSocket opened")

    async def on_message(self, message):
        await Message.create(text=message)
        self.write_message(message)

    def on_close(self):
        print("WebSocket closed")


