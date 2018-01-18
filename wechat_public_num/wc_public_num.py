#!/usr/bin/env python
# coding=utf-8
from __future__ import with_statement
import sys
import activity
import os
from com.android.monkeyrunner import MonkeyRunner as mr
from com.android.monkeyrunner.recorder import MonkeyRecorder as recorder


tmp = "tmp/"
STATUS_SUFFIX = ".task.status"
DOWN_AND_UP = 'DOWN_AND_UP'
PUBLIC_NUM_PLATFORM_PATH = tmp + 'focused_public_num_platform_json'

wc_id = "smartisan2013"
wc_name = "smartisan2013"

if len(sys.argv) == 2:
    wc_id = sys.argv[1]
    wc_name = sys.argv[2]

if not os.path.exists(PUBLIC_NUM_PLATFORM_PATH):
    with open(PUBLIC_NUM_PLATFORM_PATH, "wb") as fp:
        fp.write("{}")

device = mr.waitForConnection()
if not device:
    print >> sys.stderr, "fail"
    sys.exit(1)

print "connected ..."

recorder.start(device)

drag_count = 0


def has_focus_public_num_platform(public_num_platform_id):
    with open(PUBLIC_NUM_PLATFORM_PATH, "r") as focus_fp:
        pnpJson = focus_fp.read()

    focus = public_num_platform_id in pnpJson

    if not focus:
        with open(PUBLIC_NUM_PLATFORM_PATH, "a") as focus_fp:
            focus_fp.write(public_num_platform_id+"--wc--pp--")

    return focus


def continue_drag():
    # 每滑动20次，就去读取下文件
    global drag_count

    if drag_count == 0 or drag_count > 2000 or drag_count % 20 != 0:
        return True
    drag_count = drag_count + 1

    with open(tmp + wc_name + ".task.status", 'wb') as status_f:
        status = status_f.read()

    return status == "1"


def enter_history_message():
    # view history
    # device.touch(335, 834, DOWN_AND_UP)
    os.system("./uiauto.py")
    mr.sleep(2)

    while continue_drag():
        device.drag((150, 410), (150, 110), 1, 10)
        mr.sleep(3)

    print "drag finish ..."
    # 点击历史消息界面返回按钮
    device.touch(49, 96, DOWN_AND_UP)
    mr.sleep(1)
    # 点击公众号详情界面返回按钮
    device.touch(49, 96, DOWN_AND_UP)
    mr.sleep(1)
    # 点击公众号聊天界面返回按钮
    device.touch(49, 96, DOWN_AND_UP)


def search_public_num(public_num_wechat_id):
    # 清空输入文本
    device.touch(668, 93, DOWN_AND_UP)
    # 触摸输入框
    device.touch(375, 90, DOWN_AND_UP)
    device.type(public_num_wechat_id)
    mr.sleep(1)
    # 触摸搜索
    device.touch(663, 1104, DOWN_AND_UP)
    mr.sleep(5)
    # 触摸搜索出的股票进详情
    device.touch(346, 330, DOWN_AND_UP)
    mr.sleep(2)


wc_home_name = "com.tencent.mm/com.tencent.mm.ui.LauncherUI"
# 启动特定的Activity
device.startActivity(component=wc_home_name)

current = activity.get_current_activity()
device = mr.waitForConnection()
mr.sleep(1)

if current.count("FTSSearchTabWebViewUI") != 0:
    print 'at search public_number_platform page'
    device = mr.waitForConnection()
    mr.sleep(2)
    search_public_num(wc_id)
elif current.count("BrandServiceIndexUI") != 0:
    print 'at public_number_platform page'
    device = mr.waitForConnection()
    # 点击公众号页面的加号
    device.touch(654, 104, DOWN_AND_UP)
    mr.sleep(2)
    search_public_num(wc_id)
elif current.count("ContactInfoUI") != 0:
    device = mr.waitForConnection()
    mr.sleep(2)
    enter_history_message()
else:
    device = mr.waitForConnection()
    # 点击首页的通讯录页签
    device.touch(272, 1133, DOWN_AND_UP)
    mr.sleep(1)
    # 点击通讯录的公众号标签
    device.touch(360, 528, DOWN_AND_UP)
    mr.sleep(1)
    # 点击公众号页面的加号
    device.touch(654, 104, DOWN_AND_UP)
    mr.sleep(1)
    search_public_num(wc_id)
