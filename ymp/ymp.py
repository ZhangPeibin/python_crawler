#!/usr/bin/env python
#coding=utf-8
import re
from bs4 import BeautifulSoup
import time
import threading
from multiprocessing import Pool
import multiprocessing
import logging
import sys
import os
import sql
import Queue
import http

sys.setrecursionlimit(10000000)

urls=[]

UNUSED_PATH = [None,"/","#","javascript:void(0)"]

root = 'http://www.yemalu.pw'
videotype=1
url = root+'/videos?c=%d&page=%d&o=tf'
config_url = root+"/media/player/config_v.php?vkey=%s-1-1"

processCount=10

class UrlModel(object):
        def __init__(self,title,url,config_url,watch,good):
                self.title = title
                self.mp4_url = url
                self.config_url=config_url
                self.watch = watch
                self.good = good


def process_web(ul,httpClient,queue):
    soup = BeautifulSoup(str(ul))

    good = soup.find_all(text=re.compile("\d+\%",re.M|re.I))
    if not good:
        good = "-"
    else:
        good = good[0]
    
    goodNum = re.search("\d+",good,re.M|re.I)
    if not goodNum:
        return

    goodNum = int(goodNum.group())

    if goodNum < 66:
        return

    a = soup.find_all('a',limit=1)
    if not a:
        return   
    url = a[0]['href']
    number = re.search("\d+",url,re.M|re.I).group()
    curl = config_url % number
    if curl in urls:
        return
    urls.append(curl)
    r =httpClient.http_get(curl,retries=3)
    if r == None:
        print "check faile" 
        return

    r.encoding = 'utf-8'
    url = r.text
    if not http.checkUrl(url):
        return
    else:
        pass
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
    urlModel = UrlModel(title,url,curl,watch,good)
    queue.put(urlModel)

def formatUrl(page):
    return url % (videotype,page)

def get_all_url(start,end,queue,hc=None,retries = 3):#递归爬取所有url 
    if start == end-1:
        print "finish job between %d to %d"%(start,end)
        return

    if not hc:
        hc = http.YmlHttp()

    if not queue:
        queue = Queue.Queue()

    currentUrl = formatUrl(start)
    print '[%s] process... %s' % (os.getpid(),currentUrl)

    r = hc.http_get(currentUrl)
    
    if r == None :
        if retries > 0:
            get_all_url(start,end,queue,hc,retries-1)
        else:
            print "process  %s with response none" % url
            print '...'
            get_all_url(start+1,end,queue,hc)
        return 

    r.encoding = 'utf-8'
    
    soup = BeautifulSoup(r.text, "html.parser")
    allA = soup.find_all('div','col-sm-6 col-md-4 col-lg-4') 
    
    if  (not allA):
            print "get a empty <a> tag from %s " % uri
            get_all_url(start+1,end,hc,queue)
            return
        
    th=[]

    for k in allA:
        t = threading.Thread(target=process_web,args=(k,hc,queue))
        t.start()
        th.append(t)
    
    for t in th:
        t.join()

    get_all_url(start+1,end,queue,hc)


def dispatch_tasks(total):
    if total <= 0:
        return
    totalPage = total/18
    perCount = totalPage/ processCount
    
    pool = Pool()
    queues = []
    manager = multiprocessing.Manager()
    for i in range(processCount):
        start = i * perCount+3
        if i == processCount-1:
            end = totalPage+1
        else:
            end = (i+1) * perCount+2
        q = manager.Queue()
        queues.append(q)
        print "%s - %s " %(start,end)
        #pool.apply_async(get_all_url,args=(start,end,q))

    pool.close()
    pool.join()
    
    db = sql.SqlHelper()
    for q in queues:
        try:
            while q.qsize() > 0:
                model = q.get(block = False)
                db.save_to_db(model.title,model.mp4_url,model.config_url,model.watch,model.good)
        except Exception as e:
            logging.exceptione()

    print "All subprocesses done."
        
    

def begin(rooturl,retries=3,httpclient=None):
    if httpclient == None:
        httpClient = http.YmlHttp()
    print 'process first page ... %s' % rooturl 
    r = httpClient.http_get(rooturl)    
    if r == None :
        if retries > 0:
            begin(rooturl,retries-1,httpClient)
        else:
            print "process  %s with response none" % url
        return 

    r.encoding = 'utf-8'
    
    soup = BeautifulSoup(r.text, "html.parser")
    allA = soup.find_all('div','col-sm-6 col-md-4 col-lg-4') 
    
    textwhite = soup.find_all("span",'text-white')
    total = int(textwhite[len(textwhite)-1].string)-18

    th=[]
    q = Queue.Queue()
    db = sql.SqlHelper()
    for k in allA:
        t = threading.Thread(target=process_web,args=(k,httpClient,q))
        t.setDaemon(True)
        t.start()
        th.append(t)

    for t in th:
        t.join()
    try:
        while q.qsize() > 0:
            model = q.get(block = False)
            db.save_to_db(model.title,model.mp4_url,model.config_url,model.watch,model.good)
    except Exception as e:
        logging.exceptione()

    dispatch_tasks(total)

begin(url%(videotype,1))
