#!/usr/bin/env python
#coding=utf-8
import sqlite3


db_name = "91.db"
table_name = "mp4"

class Column():

    def __init__(self):
        pass

    videourl = "url"
    videoname = "name"
    videotime = "time"
    addtime = "addtime"
    author = "author"
    authorurl = "authorurl"
    views = "views"
    likes = "likes"
    comments = "comments"


class SqlHelper(object):
    
    def __init__(self):
        self.__conn__ = sqlite3.connect(db_name)
        self.__conn__.execute("CREATE TABLE IF NOT EXISTS %s  \
                (%s TEXT, %s TEXT,%s TEXT,%s TEXT,%s Text,%s Text,%s Text,%s Text,%s Text)" % (table_name,
                 Column.videourl, Column.videoname, Column.videotime, Column.addtime, Column.author,Column.authorurl, Column.views, Column.likes, Column.comments))
    
    def save_to_db(self,url,name,time,addtime,author,authorurl,views,likes,comments):
        self.__conn__.execute('INSERT INTO %s (%s,%s,%s,%s,%s,%s,%s,%s,%s) VALUES (?,?,?,?,?,?,?,?,?)'
           %(table_name, Column.videourl, Column.videoname, Column.videotime, Column.addtime, Column.author,Column.authorurl, Column.views, Column.likes, Column.comments)
           ,(url, name, time, addtime, author, authorurl, views, likes, comments))
        self.__conn__.commit()
    

if __name__ == "__main__":
    sqlHelper = SqlHelper()
    sqlHelper.save_to_db("1","2","3","4","5","6","7","8","9")
