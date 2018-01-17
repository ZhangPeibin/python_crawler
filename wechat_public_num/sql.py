#!/usr/bin/env python
# coding=utf-8
import sqlite3

db_name = "public_num.db"


class Column:
    def __init__(self):
        pass

    TITLE = "title"
    TIME = "time"
    ID = "id"
    COVER = 'cover'
    PATH = 'PATH'


class SqlHelper(object):

    def __init__(self, table_name):
        self.__table_name__ = table_name
        self.__conn__ = sqlite3.connect(db_name)
        self.__conn__.text_factory = str
        self.__conn__.execute('''CREATE TABLE IF NOT EXISTS %s  \
                (%s TEXT, %s TEXT,%s TEXT ,%s TEXT ,%s TEXT)''' %
                              (table_name, Column.TITLE, Column.TIME, Column.ID, Column.COVER, Column.PATH))

    def save_to_db(self, title, time, id, cover, path):
        self.__conn__.execute('INSERT INTO %s (%s,%s,%s,%s,%s) VALUES (?,?,?,?,?)'
                              % (self.__table_name__, Column.TITLE, Column.TIME, Column.ID, Column.COVER, Column.PATH)
                              , (title, time, id, cover, path))
        self.__conn__.commit()

    def get_from_db(self):
        cur = self.__conn__.execute("SELECT %s,%s,%s,%s,%s from %s" %
                                    (Column.TITLE, Column.TIME, Column.ID, Column.COVER, Column.PATH, self.__table_name__))
        return list(cur)
