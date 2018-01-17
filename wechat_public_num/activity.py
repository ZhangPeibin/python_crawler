#!/usr/bin/env python
# coding=utf-8
import os
import time

def get_current_activity():
    os.system('adb shell dumpsys activity | grep mFocusedActivity > ./tmp/activity.txt')
    f = open("tmp/activity.txt", 'r').read()
    a = f.split('/')
    result = a[1].split(' ')
    return result[0]


def is_current_at_weixin():
    os.system('adb shell dumpsys activity | grep mFocusedActivity > ./tmp/activity.txt')
    time.sleep(2)
    f = str(open("tmp/activity.txt", 'r').read())
    count = f.count("tencent")
    return count != 0
