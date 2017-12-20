#!/usr/bin/env python
#coding=utf-8
import sqlite3


db_name = "db_ymp.db"
table_name = "cn_mp4"

class Column():
    TITLE = "title"
    MP4_URL = "mp4_url"
    CONFIG_URL = "config_url"
    WATCH = "watch"
    GOOD = "good"

class SqlHelper(object):
    
    def __init__(self):
        self.__conn__ = sqlite3.connect(db_name)
        self.__conn__.execute('''CREATE TABLE IF NOT EXISTS %s  \
                (%s TEXT, %s TEXT,%s TEXT,%s TEXT,%s Text)''' % \
                (table_name,Column.TITLE,Column.MP4_URL,Column.CONFIG_URL,Column.WATCH,Column.GOOD))   
    

    def save_to_db(self,title,mp4_url,config_url,watch="-",good="-"):
        self.__conn__.execute('INSERT INTO %s (%s,%s,%s,%s,%s) VALUES (?,?,?,?,?)' \
           %(table_name,Column.TITLE,Column.MP4_URL,Column.CONFIG_URL,Column.WATCH,Column.GOOD)\
           ,(title,mp4_url,config_url,watch,good))
        self.__conn__.commit()
    
    def get_from_db(self,limit,offset):
        cur = self.__conn__.execute("SELECT %s,%s,%s,%s from %s limit %d OFFSET %d" %
                (Column.TITLE,Column.MP4_URL,Column.CONFIG_URL,Column.GOOD,table_name,limit,offset))
        return list(cur)

if __name__ == "__main__":
    sqlHelper = SqlHelper()
    sqlHelper.save_to_db("1","2","3","4","5")
    print sqlHelper.get_from_db(10,0)
