#!/usr/bin/env python
#coding=utf-8

def download_1():
    cur = conn.execute("SELECT title,url from %s  limit %d OFFSET %d" % (table_name,limit,offset))
    for row in cur:
        down(row)    
        time.sleep(1)

    print "Sub-process(es) down"
   


def download():
    th=[]
    for row in cur:
        t = threading.Thread(target=down,args=(row,))
        th.append(t)
        t.start()
        if threading.activeCount() > 3:
                time.sleep(1)

    for t in th:
        t.join()

    print "Sub-process(es) down"
   


#get_all_url(next())

download_1()
