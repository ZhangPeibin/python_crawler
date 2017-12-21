#!/usr/bin/env python
#coding=utf-8
import requests
import os
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from tqdm import tqdm
import urllib2
import logging
import httplib
import urlparse


headers = {
    "User-Agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Mobile/14E304  MicroMessenger/6.5.12 NetType/WIFI Language/zh_CN",
    "Connection": "keep-alive",
    "Accept-Encoding": "gzip, deflate",
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
}

codes = [302,200]

class YmlHttp(object):

    def __init__(self):
        self.HTTP_SESSION = requests.session()
        self.HTTP_SESSION.headers.update(headers)
        self.retry = Retry(connect=3,
                backoff_factor=0.5)
        self.adapter = HTTPAdapter(max_retries=self.retry,pool_connections=200,pool_maxsize=300)
        self.HTTP_SESSION.mount('http://', self.adapter)
        self.HTTP_SESSION.mount('https://', self.adapter)
        self.proxies = {
            "http":"http://118.193.107.37:80",
            }

    def http_get(self,url, params={},retries=0):
            try:
                r = self.HTTP_SESSION.get(url, params=params)
                if r.status_code == 200:
                    return r
                else:
                    if str(r.status_code).startswith("5") and retries > 0:
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

    def http_download_process(self,title,mp4_url,config_url,retries=3):
        if not os.path.exists('./mp4_yml'):
            os.mkdir("./mp4_yml")

        file_size = int(urllib2.urlopen(mp4_url).info().get('Content-Length', -1))

        if os.path.exists('./mp4_yml/%s.mp4'%title):
            first_byte = os.path.getsize('./mp4_yml/%s.mp4'%title)
        else:
            first_byte = 0
    
        if first_byte >= file_size:
            return

        if first_byte != 0:
            os.remove("./mp4_yml/%s.mp4"%title)
            first_byte = 0

        #header = {"Range": "bytes=%s-%s" % (first_byte, file_size)}
        
        pbar = tqdm(
            total=file_size, initial=first_byte,
            unit='B', unit_scale=True, desc=mp4_url.split('/')[-1])

        try:
            res = self.HTTP_SESSION.get(mp4_url,stream=True)
            #res = HTTP_SESSION.get(mp4_url,proxies=proxies,params=header,stream=True)
        except Exception as e:
            #may be can not access
            logging.exception(e)
            if errorretries > 0:
                try:
                    conres = http_get(config_url)
                    conres.coding='utf-8'
                    if conres.status == 200:
                        http_download(title,conres.text,config_url,retries,errorretries-1)
                    else:
                        print 'can not connect to %s' % path
                except:
                    logging.exception(e)
                else:
                    time.sleep(2)
                    logging.exception(e)
        else:
            if res.status_code == 200:
                with open('./mp4_yml/%s.mp4' % title,'wb') as f:
                    for chunk in res.iter_content(chunk_size=1024):
                        if not (chunk == None):
                            f.write(chunk)
                            pbar.update(1024)
            else:
                if str(res.status_code).startswith("5") and retries > 0:
                    http_download(row,retries-1)
                else:
                    print "response code : %d" % res.status_code
        finally:
            pbar.close()

    def http_download(self,title,mp4_url,config_url,retries=3,errorretries=1):
            print path
            if not os.path.exists('./mp4_yml'):
                os.mkdir("./mp4_yml")

            if not os.path.exists('./mp4_yml/%s.mp4'%title):        
                try:
                    res = self.HTTP_SESSION.get(mp4_url,stream=True)
                    #res = HTTP_SESSION.get(path,proxies=proxies,stream=True)
                except Exception as e:
                    #may be can not access
                    logging.exception(e)
                    if errorretries > 0:
                        print "retry connect"
                        try:
                            conres = http_get(config_url)
                            conres.coding='utf-8'
                            if conres.status == 200:
                                http_download(title,conres.text,config_url,retries,errorretries-1)
                            else:
                                print 'can not connect to %s' % path
                        except:
                            logging.exception(e)
                    else:
                        time.sleep(2)
                        logging.exception(e)
                else:
                    if res.status_code == 200:
                        with open('./mp4_yml/%s.mp4' % title,'wb') as f:
                            for chunk in res.iter_content(chunk_size=1024):
                                if chunk:
                                    f.write(chunk)
                                    f.flush()
                    else:
                        if str(res.status_code).startswith("5") and retries > 0:
                            http_download(row,retries-1)
                        else:
                            print "response code : %d" % res.status_code
                finally:
                    print "%s finish" % path
            else :
                print "%s exists" % path




def checkUrl(url):
    if len(url) == 0 :
        return False

    host,path = urlparse.urlparse(url)[1:3]
    conn = None
    try:
        conn = httplib.HTTPConnection(host)
        conn.request("HEAD",path)
        code = conn.getresponse().status
        if  code in codes:
            return True
        else:
            return False
    except Exception as e:
        logging.exception(e)
        return False
    finally:
        if conn :
            conn.close()

if __name__ == '__main__':
    print checkUrl("http://adultvideo.science/media/videos/iphone/170.mp4")

    ht = YmlHttp()
    ht.http_download_process("test","http://adultvideo.science/media/videos/iphone/170.mp4","|http://101.96.8.142/adultvideo.science/media/videos/iphone/808.mp4")







