#!/usr/bin/env python
#coding=utf-8
import re
from bs4 import BeautifulSoup
import requests
import os
import time
import threading
import sqlite3
import logging
import sys

sys.setrecursionlimit(10000000)

db_name = "db_ymp.db"
table_name = "mp4"
conn = sqlite3.connect(db_name)
conn.execute('''CREATE TABLE IF NOT EXISTS %s (title TEXT, url TEXT,watch TEXT,good Text)''' % table_name)     
  
def save_to_db(title,url,watch="-",good="-"):
   conn.execute('INSERT INTO %s (title,url,watch,good) VALUES    \
           (?,?,?,?)' % table_name ,(title,url,watch,good))
   conn.commit()

urls=[]
models = []

UNUSED_PATH = [None,"/","#","javascript:void(0)"]
HTTP_SESSION = requests.session()
HTTP_SESSION.headers.update({"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Mobile/14E304 MicroMessenger/6.5.12 NetType/WIFI Language/zh_CN"})

page = 0
root = 'http://www.yemalu.pw'
url = root+'/videos?page=%d'
config_url = root+"/media/player/config_v.php?vkey=%s-1-1"

class UrlModel(object):
        def __init__(self,title,url,watch,good):
                self.title = title
                self.url = url
                self.watch = watch
                self.good = good


def http_get(url, params={},retries=0):
        try:
            r = HTTP_SESSION.get(url, params=params)
            if r.status_code == 200:
                return r
            else:
                if retries > 0:
                    http_get(url,params,retries-1)
                else:
                    print "%s request failed %d " % (url,r.status_code)
                    return None
        except Exception as e:
            if retries > 0:
                    http_get(url,params,retries-1)
            else:
                logging.exception(e)
            return None

def dispatch_web_process(ul):
    soup = BeautifulSoup(str(ul))
    a = soup.find_all('a',limit=1)
    if not a:
        return   
    url = a[0]['href']
    number = re.search("\d+",url,re.M|re.I).group()
    url = config_url % number
    r = http_get(url,retries=3)
    if r == None:
        return
    r.encoding = 'utf-8'
    url = r.text
    title=""
    titletag = soup.find_all("span",limit=1)
    if titletag :
        title = titletag[0].string
    else:
        title = url.rsplit("/",-1)

    watchdiv = soup.find_all("div","video-views",limit=1)
    watch = ""
    if watchdiv:
        watch = watchdiv[0].string.lstrip().rstrip()
    good = soup.find_all(text=re.compile("\d+\%",re.M|re.I))
    if not good:
        good = "-"
    else:
        good = good[0]

    urlModel = UrlModel(title,url,watch,good)
    models.append(urlModel)

def dispatch_url_cache(url):
    urls.append(url)


def next():
    global page
    page = page +1
    return url % page

def get_next_url_and_navigation(soup):
    nexts = soup.find_all("ul","pagination")

    if not nexts:
        get_all_url(next())
        return

    ul = nexts[0]
    
    if ul == None:
        return

    li = soup.find_all("a","prevnext")
    
    if not li:
        print "process finish"
        return

    nexturl = li[0]['href']

    match = re.search("page=\d+",nexturl,re.M|re.I)
    global page
    if match :
        n = re.search("\d+",match.group(),re.M|re.I)
        p = int(n.group())
        if p == page+1:
            get_all_url(next())
        elif p==page:
            print 'process finish'
        else:
            page = p -1
            get_all_url(next())
            
    else:
        get_all_url(next())




def get_all_url(url,retries = 3):#递归爬取所有url    
    #初始化
    print 'process... %s' % url 
    
    r = http_get(url)
    
    if r == None :
        if retries > 0:
            get_all_url(url,retries-1)
        else:
            print "process  %s with response none" % url
            print '...'
            get_all_url(next())
        return 

    r.encoding = 'utf-8'
    
    soup = BeautifulSoup(r.text, "html.parser")
    allA = soup.find_all('div','col-sm-6 col-md-4 col-lg-4') 
    
    if len(url) == 0 and (not allA):
            print "get a empty <a> tag from %s " % uri
            get_all_url(next())
            return
        
    th=[]
    for k in allA:
        t = threading.Thread(target=dispatch_web_process,args=(k,))
        t.setDaemon(True)
        t.start()
        th.append(t)
        if threading.activeCount() > 5:
            time.sleep(2)
    

    for t in th:
        t.join()

    global models

    for model in models:
            save_to_db(model.title,model.url,model.watch,model.good)

    models = []

    time.sleep(3)

    get_next_url_and_navigation(soup)

get_all_url(next())

