#!/usr/bin/env python
# coding=utf-8
import os
import time


def get_current_activity():
    os.system('adb shell dumpsys activity | grep mFocusedActivity > ./tmp/activity.txt')
    f = open("./tmp/activity.txt", 'r').read()
    a = f.split('/')
    result = a[1].split(' ')
    return result[0]


def is_current_at_weixin():
    os.system('adb shell dumpsys activity | grep mFocusedActivity > ./tmp/activity.txt')
    time.sleep(2)
    f = str(open("./tmp/activity.txt", 'r').read())
    count = f.count("tencent")
    return count != 0


def start_weixin_app():
    code = os.system('adb shell am start -n "com.tencent.mm/com.tencent.mm.ui.LauncherUI" -a '
                     'android.intent.action.MAIN -c '
                     'android.intent.category.LAUNCHER')
    time.sleep(10)


def kill_weixin_app():
    code = os.system('adb shell am force-stop com.tencent.mm')

