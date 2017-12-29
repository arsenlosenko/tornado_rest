
from gino import Gino

db = Gino()


class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer(), primary_key=True)
    book = db.Column(db.Unicode(), default='none')
    author = db.Column(db.Unicode(), default='none')


class Price(db.Model):
    __tablename__ = 'prices'
    id = db.Column(db.Integer(), primary_key=True)
    book = db.Column(db.Unicode(), default='none')
    price = db.Column(db.Integer(), default=0)


class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer(), primary_key=True)
    date = db.Column(db.Date)
    text = db.Column(db.Unicode(), default="none")
