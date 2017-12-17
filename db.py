#!/usr/bin/env python
#coding=utf-8

import sqlite3

class DbHelper(object):

        def __init__(self,db_name):
            self.__conn__ = sqlite3.connect(db_name)
            if len(self.__conn__.execute("SELECT * FROM sqlite_master WHERE type='table' and name='xsp'").fetchall()) == 0:
               self.__conn__.execute('''CREATE TABLE IF NOT EXISTS videourls (title TEXT, url TEXT)''')           
  
        def save_to_db(self,title,url):
            self.__conn__.execute('INSERT INTO videourls (title,url) VALUES (?,?)',(title,url))
            self.__conn__.commit()

