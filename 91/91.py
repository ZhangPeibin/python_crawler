#!/usr/bin/env python
# coding=utf-8
import Queue
import threading
import logging
from bs4 import BeautifulSoup
from lxml import etree
import model
import multiprocessing
from multiprocessing import Pool
import os
import ninesql

import sys

sys.path.append("..")
import ymp.http as http

client = http.YmlHttp()

url = "http://93.91p12.space/v.php?category=mf&viewtype=basic&page=%s"


def process_web(soup, q, hc):
    videoContentList = soup.find('div', attrs={'id': 'videobox'})
    i = 0
    selector = etree.HTML(soup.prettify())

    for videoLi in videoContentList.find_all('div', attrs={'class': 'listchannel'}):

        videoName = videoLi.find('img', attrs={'width': '120'}).get('title')

        videoUrl = videoLi.find('a', attrs={'target': 'blank'}).get('href')
        # r = hc.http_get(videoUrl)
        # if r is None:
        #     print 'none'
        #     continue
        #
        # videoSouceSoup = BeautifulSoup(r.text)
        # href = videoSouceSoup.find_all("source")
        # print href
        timetext = selector.xpath('//div[@class="listchannel"]/text()')[4 + i * 17].strip()
        addtimetext = selector.xpath('//div[@class="listchannel"]/text()')[6 + i * 17].strip()
        try:
            videoAuthorContent = videoLi.find('a', attrs={'target': '_parent'}).getText()
        except AttributeError:
            videoAuthorContent = "None"

        try:
            videoAuthorUrl = videoLi.find('a', attrs={'target': '_parent'}).get('href')
        except AttributeError:
            videoAuthorUrl = "None"
        viewNumber = selector.xpath('//div[@class="listchannel"]/text()')[10 + i * 17].strip()
        likeNumber = selector.xpath('//div[@class="listchannel"]/text()')[11 + i * 17].strip()
        commentNumber = selector.xpath('//div[@class="listchannel"]/text()')[13 + i * 17].strip()

        videoInfo = model.VideoModel(videoUrl, videoName, timetext, addtimetext,
                                     videoAuthorContent, videoAuthorUrl, viewNumber, likeNumber, commentNumber)
        q.put(videoInfo)


def formatUrl(page):
    return url % page


def poolPage(startPage, endPage, hc, q, flag, retries=3):
    if startPage == endPage - 1:
        print "finished job between %s to %s " % (startPage, endPage)
        return

    if hc is None:
        hc = http.YmlHttp()

    currentUrl = formatUrl(startPage)

    print '[%s] process... %s' % (os.getpid(), currentUrl)

    r = hc.http_get(currentUrl)

    if r is None:
        if retries > 0:
            poolPage(startPage, endPage, hc, q, flag, retries - 1)
        else:
            print "process  %s with response none" % url
            print '...'
            poolPage(startPage + 1, endPage, hc, q, flag, retries)
        return

    soup = BeautifulSoup(r.text, "html.parser")
    process_web(soup, q,hc)

    poolPage(startPage + 1, endPage, hc, q, flag, retries)


def process_queue(q, flag):
    db = ninesql.SqlHelper()

    while len(flag) > 0:
        if q.qsize() > 0:
            model = q.get(block=True)
            db.save_to_db(model.videourl, model.videoname, model.videotime, model.addtime, model.author,
                          model.authorurl,
                          model.views, model.likes, model.comments)

    while q.qsize() > 0:
        model = q.get(block=True)
        db.save_to_db(model.videourl, model.videoname, model.videotime, model.addtime, model.author, model.authorurl,
                      model.views, model.likes, model.comments)


def dispatch_task(page):
    if page < 0:
        return

    processCount = 10
    perCount = page / 10

    manager = multiprocessing.Manager()
    pool = Pool()
    q = manager.Queue()
    flag = manager.list()
    for i in range(processCount):
        start = i * perCount + 1
        if i == processCount - 1:
            end = page + 1
        else:
            end = (i + 1) * perCount + 1
        flag.append(i)
        pool.apply_async(poolPage, args=(start, end, None, q, flag))

    t = threading.Thread(target=process_queue, args=(q, flag))
    t.start()
    t.join()

    pool.close()
    pool.join()
    print "All subprocesses done."


def getPageCount(soup):
    videoPaging = soup.find_all("div", attrs={"class": "videopaging"})[0].text
    page = int(videoPaging.split("of")[1].strip()) / 20 - 1
    return page


def begin():
    r = client.http_get(url % 0, retries=3)

    if r is None or r.status_code != 200:
        print "can not fetch main page"
        return
    r.coding = 'utf-8'

    print "process main page"

    soup = BeautifulSoup(r.text, "html.parser")

    page = getPageCount(soup)

    dispatch_task(page)

    q = Queue.Queue()
    t = threading.Thread(target=process_web, args=(soup, q,r))
    t.setDaemon(True)
    t.start()

    t.join()

    try:
        while q.qsize() > 0:
            m = q.get(block=False)
            # saving
            # print m
    except Exception as e:
        logging.exception(e)


begin()
