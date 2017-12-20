#!/usr/bin/env python
#coding=utf-8
import re
from bs4 import BeautifulSoup
import time
import threading
from multiprocessing import Pool
import logging
import sys
from tqdm import tqdm

import sql
import http

sys.setrecursionlimit(10000000)

sql = sql.SqlHelper()

urls=[]
models = []

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


def process_web(ul):
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
    r =http.http_get(curl,retries=3)
    if r == None:
        return
    r.encoding = 'utf-8'
    url = r.text
    if not http.checkUrl(url):
        return
    else:
        pass
        #print "use url %s " % url

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
    models.append(urlModel)


def formatUrl(page):
    return url % (videotype,page)

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


def get_all_url(start,end,retries = 3):#递归爬取所有url 
    if start == end-1:
        print "finish job between %d to %d"%(start,end)
        return

    currentUrl = formatUrl(start)
    print 'process... %s' % currentUrl 

    r = http.http_get(currentUrl)
    
    if r == None :
        if retries > 0:
            get_all_url(start,end,retries-1)
        else:
            print "process  %s with response none" % url
            print '...'
            get_all_url(start+1,end)
        return 

    r.encoding = 'utf-8'
    
    soup = BeautifulSoup(r.text, "html.parser")
    allA = soup.find_all('div','col-sm-6 col-md-4 col-lg-4') 
    
    if  (not allA):
            print "get a empty <a> tag from %s " % uri
            get_all_url(start+1,end)
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
            sql.save_to_db(model.title,model.url,"--",model.watch,model.good)

    models = []

    time.sleep(3)
    
    get_all_url(start+1,end)




def dispatch_tasks(total):
    if total <= 0:
        return
    perCount = total /18/ processCount

    pool = Pool()
    for i in range(processCount):
        start = i * perCount+2
        if i == processCount-1:
            end = total
        else:
            end = (i+1) * perCount+2
        pool.apply_async(get_all_url,args=(start,end))

    pool.close()
    pool.join()

    print "All subprocesses done."
        
    

def begin(rooturl,retries=3):
    print 'process first page ... %s' % rooturl 
    r = http.http_get(rooturl)    
    if r == None :
        if retries > 0:
            begin(rooturl,retries-1)
        else:
            print "process  %s with response none" % url
        return 

    r.encoding = 'utf-8'
    
    soup = BeautifulSoup(r.text, "html.parser")
    allA = soup.find_all('div','col-sm-6 col-md-4 col-lg-4') 
    
    textwhite = soup.find_all("span",'text-white')
    total = int(textwhite[len(textwhite)-1].string)-18

    th=[]
    for k in allA:
        t = threading.Thread(target=process_web,args=(k,))
        t.setDaemon(True)
        t.start()
        th.append(t)

    for t in th:
        t.join()

    global models

    for model in models:
            sql.save_to_db(model.title,model.mp4_url,model.config_url,model.watch,model.good)

    models = []

    dispatch_tasks(total)

begin(url%(videotype,1))
