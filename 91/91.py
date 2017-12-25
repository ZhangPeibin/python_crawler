#!/usr/bin/env python
#coding=utf-8
import sys
import Queue
import threading
import logging

sys.path.append("..")

import ymp.http as http

from bs4 import BeautifulSoup

from lxml import etree

client = http.YmlHttp()


page = 0
url = "http://93.91p12.space/v.php?category=mf&viewtype=basic&page=%s"


def process_web(soup,q):
    videoContentList=soup.find('div',attrs={'id':'videobox'})
    #print(videoContentList)#可以打印出来
    videoInfoList=[]
    i=0
    selector=etree.HTML(soup.prettify())
    
    for videoLi in videoContentList.find_all('div',attrs={'class':'listchannel'}):
        
        videoName=videoLi.find('img',attrs={'width':'120'}).get('title')
        videoUrl=videoLi.find('a',attrs={'target':'blank'}).get('href')

        timetext=selector.xpath('//div[@class="listchannel"]/text()')[4+i*17].strip()
        addtimetext=selector.xpath('//div[@class="listchannel"]/text()')[6+i*17].strip()
        try:
            videoAuthorContent=videoLi.find('a',attrs={'target':'_parent'}).getText()
        except AttributeError:
            videoAuthorContent="None"
        
            
        #print(videoUrl+str(i))
        try:
            videoAuthorUrl=videoLi.find('a',attrs={'target':'_parent'}).get('href')
        except AttributeError:
            videoAuthorUrl="None"
        viewNumber=selector.xpath('//div[@class="listchannel"]/text()')[10+i*17].strip()
        likeNumber=selector.xpath('//div[@class="listchannel"]/text()')[11+i*17].strip()
        commentNumber=selector.xpath('//div[@class="listchannel"]/text()')[13+i*17].strip()
        
        videoInfoList.append(videoUrl)#链接
        videoInfoList.append(videoName)#视频名
        videoInfoList.append(timetext)#视频时长
        videoInfoList.append(addtimetext)#上传时间
        videoInfoList.append(videoAuthorContent)#上传者id
        videoInfoList.append(videoAuthorUrl)#上传者主页
        videoInfoList.append(viewNumber)#观看数
        videoInfoList.append(likeNumber)#收藏数
        videoInfoList.append(commentNumber)#评论数

        print videoInfoList
def dispatch_task(page):
    if page < 0:
        return


def begin():
    r = client.http_get(url%0,retries=3)
    
    if r == None or r.status_code != 200:
        print "can not fetch main page"
        return
    r.coding='utf-8'

    print "process main page"
    
    soup = BeautifulSoup(r.text,"html.parser")

    page =  soup.find_all("div",attrs={"class":"videopaging"})[0].text
    page = int(page.split("of")[1].strip())/20-1
    dispatch_task(page)

    q = Queue.Queue()
    t = threading.Thread(target=process_web,args=(soup,q))
    t.setDaemon(True)
    t.start()

    t.join()
    
    try:
        while q.qsize() > 0:
            m = q.get(block=False)
            #saving
    except Exception as e:
        logging.exception(e)



begin()

