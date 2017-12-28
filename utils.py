#!/usr/bin/env python3

import psycopg2
from config import DB_NAME, DB_HOST, DB_USER, DB_PASS


def psql_connection(func):
    def wrapper(*args):
        connection = psycopg2.connect(
            "dbname='{0}' user='{1}' password='{2}' host={3}".format(DB_NAME, DB_USER, DB_PASS, DB_HOST))
        cur = connection.cursor()

        value = func(cur, *args)

        connection.commit()
        connection.close()
        return value

    return wrapper
