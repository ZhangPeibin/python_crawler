#!/usr/bin/env python
#coding=utf-8

import requests

'下载m3u8文件并将其拼接为一个ts文件'

HTTP_SESSION = requests.session()
HTTP_SESSION.headers.update({"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Mobile/14E304 MicroMessenger/6.5.12 NetType/WIFI Language/zh_CN"})

def http_get(url,retries = 2):
    try:
        r = HTTP_SESSION.get(url)
        if r.status_code == 200:
            return r
        else:
            if retries > 0:
                print "reconnect %s" % url
                return http_get(url,retries-1)
            else:
                return None
    except:
        print "reconnect %s" % url
        if retries > 0:
            return http_get(url,retries-1)
        else:
            return None
        

def preProcess(host,content,path):
    tsSource = content.strip("\n").split("\n")
    tses = [ s for s in tsSource if not s.startswith('#')]
    with open(path,'ab') as f:
        for ts in tses:
            print "......"+ts
            r = http_get(host+ts)
            if not r == None:
                f.write(r.content)


#开始方式,需要传入m3u8的url以及ts的保存目录
def begin(url,savePath):
    print savePath
    if url == None :
        print "url == None "
        return

    r = http_get(url,5)
    
    if r == None:
        print "can not get m3u8 file"
        return
    urls = url.rsplit("/",1)
    host = urls[0]+"/"
    preProcess(host,r.content,savePath)

if __name__ == '__main__':
    begin('http://192.225.235.18:88/151222/zfxs/zfxs.m3u8','./ee_video/女友.ts')
