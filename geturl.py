#!/usr/bin/env python
#coding=utf-8
import requests

from itertools import permutations

a = list(permutations("e1e34"))

result=[]

def ping(url):
    try:
        res = requests.get('http://www.'+url+".com")
        if res.status_code == requests.codes.ok:
            result.append(url)
    except:
        pass

for ch in a:
    s = "".join(ch)
    ping(s)

print result
