#!/usr/bin/env python
#coding=utf-8
import php

'lutu6'

db_name = "lutu.db"

def get_video(soup):
     #找到所有的<source>
    allContentJr = soup.find_all(text=re.compile('<video.+><source'))
    if not allContentJr:
        return
    
    for mp4 in allContentJr:
        try:
            t = re.search(r'http.+\.mp4',mp4,re.M|re.I).group()
            title = soup.title.string
            php.save_to_db(title,t)
        except:
            pass

  

