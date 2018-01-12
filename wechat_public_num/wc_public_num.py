#!/usr/bin/env python
# coding=utf-8

import sys
from com.android.monkeyrunner import MonkeyRunner as mr
from com.android.monkeyrunner import MonkeyDevice as md
from com.android.monkeyrunner import MonkeyImage as mi
from com.android.monkeyrunner.recorder import MonkeyRecorder as recorder
from com.android.monkeyrunner.easy import By  as by

device = mr.waitForConnection()
if not device:
    print >> sys.stderr, "fail"
    sys.exit(1)


def search_public_num(public_num_wechat_id, clear_flag=True):
    # 触摸输入框
    device.touch(375, 90, "DOWN_AND_UP")
    if clear_flag:
        # 清空输入文本
        device.touch(668, 93, "DOWN_AND_UP")
    device.type(public_num_wechat_id)
    mr.sleep(1)
    # 触摸搜索
    device.touch(663, 1104, "DOWN_AND_UP")
    mr.sleep(3)


def start_wechat_home():
    wc_home_name = "com.tencent.mm/com.tencent.mm.ui.LauncherUI"
    # 启动特定的Activity
    device.startActivity(component=wc_home_name)


start_wechat_home()

search_public_num('smartisan2013')


recorder.start(device)

# 点第一个吧