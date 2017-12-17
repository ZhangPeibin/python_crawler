#!/usr/bin/env python
#coding=utf-8
import sqlite3
import threading
import os
import requests
import time

limit=30
page = 1
offset = page * limit

conn = sqlite3.connect('videourls.db')


HTTP_SESSION = requests.session()
HTTP_SESSION.headers.update({"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X)AppleWebKit/603.1.30 (KHTML, like Gecko) Mobile/14E304MicroMessenger/6.5.12 NetType/WIFI Language/zh_CN"})

def down(url):
    title = url[0]
    path = url[1]
    if not os.path.exists('./videos/%s.mp4'%title):
        print url[0]
        try:
            r = HTTP_SESSION.get(path,stream=True)
        except :
            pass

        if r.status_code == 200:
            with open('./videos/%s.mp4' % title,'wb') as file:
                file.write(r.content)


urls = conn.execute("SELECT title,url from videourls limit %d OFFSET %d" % (limit,offset))
for url in urls:
    threading.Thread(target=down,args=(url,)).start()  
    if threading.activeCount() > 5:
            time.sleep(5)
