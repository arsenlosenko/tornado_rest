#!/usr/bin/env python3

import psycopg2
from tornado.options import options, define, parse_config_file


class DBConnect(object):
    def __init__(self):
        define("DB_NAME", type=str)
        define("DB_HOST", type=str)
        define("DB_USER", type=str)
        define("DB_PASS", type=str)
        parse_config_file("config.py")
        self.dbname = options.DB_NAME
        self.dbhost = options.DB_HOST
        self.dbuser = options.DB_USER
        self.dbpass = options.DB_PASS
        self.connection = psycopg2.connect("dbname='{0}' user='{1}' password='{2}' host={3}"
                                           "".format(self.dbname, self.dbuser, self.dbpass, self.dbhost))
        self.cur = self.connection.cursor()

    def get_db_info(self, table):
        self.cur.execute("select * from {};".format(table))
        return self.cur.fetchall()

    def insert_book(self, book, author):
        self.cur.execute("insert into books (book, author) values ('{}', '{}')".format(book, author))
        self.cur.execute("insert into prices (book) values ('{}')".format(book))
        self.connection.commit()

    def insert_price(self, book, price):
        self.cur.execute("insert into prices (book, price) values ('{}', '{}')".format(book, price))
        self.connection.commit()

