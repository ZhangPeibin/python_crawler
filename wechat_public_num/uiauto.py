#!/usr/bin/env python
# coding=utf-8
from __future__ import with_statement
from uiautomator import device as d
import sys
import activity


tmp = "tmp/"
STATUS_SUFFIX = ".task.status"
DOWN_AND_UP = 'DOWN_AND_UP'

MIN_COUNT = 2000
MAX_COUNT = 5000
drag_count = 0

wc_search_key = "cd44444"
wc_name = "cd44444"

if len(sys.argv) == 2:
    wc_search_key = sys.argv[1]
    wc_name = sys.argv[2]

d.screen.on()

print "connected ..."


def wait_update(timeout):
    d.wait.update(timeout=timeout)


def wait_sleep(timeout):
    d.wait.idle(timeout=timeout)


def back():
    d.press.back()


def click_by_text(t, timeout=1000):
    if d(text=t).exists:
        d(text=t).click()
        wait_update(timeout=timeout)


def click_by_description(desc, timeout=1000):
    if d(description=desc).exists:
        d(description=desc).click()
        wait_update(timeout=timeout)


def reload_wei_xin():
    activity.kill_weixin_app()
    wait_update(2000)
    activity.start_weixin_app()


def continue_drag():
    # 每滑动20次，就去读取下文件
    global drag_count

    if drag_count == 0 or (drag_count < MIN_COUNT and drag_count % 20 != 0):
        drag_count = drag_count + 1
        return True

    drag_count = drag_count + 1

    with open(tmp + wc_name + ".task.status", 'r') as status_f:
        status = status_f.read()

    return status != "0" and drag_count < MAX_COUNT


def view_history_message():
    while continue_drag():
        d.swipe(150, 410, 150, 110, steps=20)


def detail_to_history_message():
    """
    处理在详情界面的操作
    1:没关注则关注
    2:进入历史消息
    :return:
    """
    has_focus = not d(text="关注").exists
    if not has_focus:
        click_by_text("关注", 3000)
        back()

    can_view_history = d(text="查看历史消息").exists

    if can_view_history:
        click_by_text("查看历史消息", 10000)
        view_history_message()


def search_public_number():
    """
    resourceId = 公众号搜索界面的editText的id
    :return:
    """
    d(resourceId="com.tencent.mm:id/hb", className='android.widget.EditText').clear_text()  # clear the text
    d(resourceId="com.tencent.mm:id/hb", className='android.widget.EditText').set_text(wc_search_key)  # set the text
    wait_update(1000)
    d.click(663, 1121)
    # 键盘的搜索
    # d.click(663, 888)
    wait_update(10000)
    # 第一个公众号的位置
    d.click(346, 330)
    wait_update(5000)
    detail_to_history_message()


def jump_search_public_number_page():
    """
    进入到微信公众号搜索界面
    :return:
    """
    current_page_str = activity.get_current_activity()
    if current_page_str.count("FTSSearchTabWebViewUI") != 0:
        print '公众号搜索界面'
        search_public_number()
    elif current_page_str.count("FTSMainUI") != 0:
        print "搜索界面"
        click_by_text("公众号")
        search_public_number()
    elif current_page_str.count("LauncherUI") != 0:
        print "首页界面"
        click_by_description("搜索", timeout=2000)
        click_by_text("公众号")
        search_public_number()
    else:
        reload_wei_xin()
        jump_search_public_number_page()


activity.start_weixin_app()
jump_search_public_number_page()
