#!/usr/bin/env python
#coding=utf-8
import re
import math
import random
import db

dbHelper = db.DbHelper('ee.db')
ipp1 = []
ipp1.append('174.128.249.100')
m01 = ipp1[int(math.floor(random.random() * len(ipp1)))] + ':88'
ipp2 = []
ipp2.append('174.128.247.9')
m02 = ipp2[int(math.floor(random.random() * len(ipp2)))] + ':88'
ipp3 = []
ipp3.append('162.221.13.140')
m03 = ipp3[int(math.floor(random.random() * len(ipp3)))] + ':88'
ipp4 = []
ipp4.append('104.193.92.25')
m04 = ipp4[int(math.floor(random.random() * len(ipp4)))] + ':88'
ipp5 = []
ipp5.append('192.225.235.18')
m05 = ipp5[int(math.floor(random.random() * len(ipp5)))] + ':88'
ipp6 = []
ipp6.append('50.117.68.115')
m06 = ipp6[int(math.floor(random.random() * len(ipp6)))] + ':88'
ipp7 = []
ipp7.append('168.235.240.236')
m07 = ipp7[int(math.floor(random.random() * len(ipp7)))] + ':88'
ipp8 = []
ipp8.append('170.178.173.110')
m08 = ipp8[int(math.floor(random.random() * len(ipp8)))] + ':88'
ipp9 = []
ipp9.append('170.178.186.10')
m09 = ipp9[int(math.floor(random.random() * len(ipp9)))] + ':88'
ipp10 = []
ipp10.append('170.178.176.80')
m10 = ipp10[int(math.floor(random.random() * len(ipp10)))] + ':88'
ipp11 = []
ipp11.append('70.39.74.133')
m11 = ipp11[int(math.floor(random.random() * len(ipp11)))] + ':88'
ipp12 = []
ipp12.append('174.128.238.133')
m12 = ipp12[int(math.floor(random.random() * len(ipp12)))] + ':88'
ip_map = {'m01': m01,
    'm02': m02,
        'm03': m03,
            'm04': m04,
                'm05': m05,
                    'm06': m06,
                        'm07': m07,
                            'm08': m08,
                                'm09': m09,
                                    'm10': m10,
                                        'm11': m11,
                                            'm12': m12}

def get_video(soup, path):
    allJr = soup.find_all(text=re.compile('http.+\\.m3u8'))
    if not allJr:
        return
    for play in allJr:
        t = re.search('http.+\\.m3u8', play, re.M | re.I).group().replace('"', '')
        tsplit = t.split('+')
        url = tsplit[0] + ip_map[tsplit[1]] + tsplit[2]
        title = soup.title.string.split('-', 1)[0]
        dbHelper.save_to_db(title, url)


def save_to_db(title, url):
    dbHelper.save_to_db(title, url)


def filter(url):
    if len(url) == 0:
        return True
    elif url.find('MOVIE03') != -1:
        return True
    elif url.find('MOVIE01') != -1:
        return True
    elif url.find('MOVIE02') != -1:
        return True
    elif url.find('list') != -1:
        return True
    else:
        return False


def cache(url):
    if url.find('list') != -1:
        return True
    else:
        return True
