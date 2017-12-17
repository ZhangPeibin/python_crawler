#!/usr/bin/env python
#coding=utf-8
import re
from bs4 import BeautifulSoup
import requests
import os
import time
import threading

import ee

urls=[]

UNUSED_PATH = [None,"/","#","javascript:void(0)"]

HTTP_SESSION = requests.session()
HTTP_SESSION.headers.update({"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Mobile/14E304 MicroMessenger/6.5.12 NetType/WIFI Language/zh_CN"})

def http_get(url, params={}):
        try:
            r = HTTP_SESSION.get(url, params=params)
            if r.status_code == 200:
                return r
            else:
                print "%s request failed %d " % (url,r.status_code)
                return None
        except:
            print "%s request except" % url
            return None


def dispatch_web_process(soup,url):
    ee.get_video(soup,url)
    #lutu.get_video(soup)
def dispatch_web_db(title,url):
    ee.save_to_db(title,url)

def dispatch_url_cache(url):
    if ee.cache(url):  
        urls.append(url)

def get_all_url(uri, url=''):#递归爬取所有url    
    if not ee.filter(url):
            return
    print 'process... %s' % url 

    r = http_get(uri+url)
    if r == None :
            print "get_all_url in %s with response none" % url
            return

    r.encoding = 'gb18030'
    
    soup = BeautifulSoup(r.text, "html.parser")
    allA = soup.find_all('a') 

    if len(url) == 0 and (not allA):
            print "get a empty <a> tag from %s " % uri

    dispatch_web_process(soup,url)
    for k in allA:
        kv = k['href']
        if kv in UNUSED_PATH:
                continue
        if ( uri in kv or (not 'http' in kv)) and kv not in urls:
            dispatch_url_cache(kv)
            get_all_url(uri, kv)
        elif re.search('http.*mp4', kv) and kv not in urls:
            dispatch_url_cache(kv)
            dispatch_web_db(soup.title.string,kv)
            print 'fuck:'+kv
            print soup.title.string

#http://www.lutu6.com
#http://www.431ee.com
get_all_url('http://www.431ee.com')

