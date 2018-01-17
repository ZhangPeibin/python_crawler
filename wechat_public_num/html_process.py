#!/usr/bin/env python
# coding=utf-8
from bs4 import BeautifulSoup
import sys
import json
import os
import time
import pycurl
import sql

reload(sys)
sys.setdefaultencoding("utf-8")

tmp = "tmp/"
this_dir_save_path = '.'+tmp+'this_dir_path'
this_dir = None
db = None
data_root = "pnp_data/"


def process_list(message_json_tuple, save_path):
    for value in message_json_tuple:

        # 纯文本
        if 'app_msg_ext_info' not in value.keys():
            continue

        app_msg_ext_info = value['app_msg_ext_info']
        comm_msg_info = value['comm_msg_info']
        content_url = str(app_msg_ext_info['content_url']).replace("&amp;amp;", "&").replace("\\", "")
        title = str(app_msg_ext_info['title']).replace('/', '／').replace('\\', '＼')
        datetime = comm_msg_info['datetime']
        wc_id = comm_msg_info['id']
        cover = app_msg_ext_info['cover'].replace("\\", "")
        c_path = os.path.join(save_path, title + ".html")
        db.save_to_db(title, datetime, wc_id, cover, c_path)
        download(c_path, content_url)
        time.sleep(2)


def process_home(content, save_path):
    start = content.index('msgList')
    end = content.index(r'if(!!window.__initCatch)')
    messageList = content[start:end]
    messageList = str(messageList[messageList.index(r'{'):messageList.rindex(r"}") + 1])
    messageList = messageList.replace("&quot;", "\"")
    messageJsonDict = json.loads(messageList, encoding='utf-8')
    messageJsonTuple = messageJsonDict['list']
    process_list(messageJsonTuple, save_path)


def process_more(content, save_path, wechat_public_num_name):
    json_data = json.loads(content)
    can_msg_continue = int(json_data['can_msg_continue'])
    general_msg_list = json.loads(json_data['general_msg_list'])
    if general_msg_list is None:
        print "error can not find list"
    messageJsonTuple = general_msg_list['list']
    process_list(messageJsonTuple, save_path)

    if can_msg_continue == 0:
        with open(tmp+wechat_public_num_name+".task.status", 'wb') as f:
            f.write("0")


def process(save_path, msg_offset):
    soup = BeautifulSoup(open(save_path))
    if soup is None:
        print "open %s err " % save_path

    # 删除tmp文件
    # os.remove(save_path)

    global this_dir
    # 公众号
    if int(msg_offset) == 0:
        wechat_public_num_name = str(soup.find('strong', 'profile_nickname').string).lstrip().rstrip()
        # wechat_public_des = str(soup.find('p', 'profile_desc').string).lstrip().rstrip()
        this_dir = data_root + wechat_public_num_name+"/"
        if not os.path.exists(this_dir):
            os.mkdir(this_dir)

        with open(this_dir_save_path, 'wb') as f:
            f.write(this_dir)
    else:
        with open(this_dir_save_path, 'r') as f:
            this_dir = f.read()
        wechat_public_num_name = this_dir.split("/")[1]

    global db
    db = sql.SqlHelper(this_dir.replace("/", "").split("-")[0])

    c_dir = this_dir + msg_offset+"/"
    if not os.path.exists(c_dir):
        os.mkdir(c_dir)

    if int(offset) == 0:
        content = soup.prettify()
        process_home(content, c_dir)
    else:
        with open(save_path, 'r') as f:
            process_more(f.read(), c_dir, wechat_public_num_name)


class WeChatNumDetails:
    def __init__(self, save_path):
        self.contents = ''
        self.save_path = save_path

    def callback(self, curl):
        self.contents = self.contents + curl
        print self.save_path
        try:
            with open(self.save_path, "wb") as f:
                f.write(self.contents)
        except Exception as e:
            print e


def download(save_path, url):
    t = WeChatNumDetails(save_path)
    c = pycurl.Curl()
    c.setopt(pycurl.WRITEFUNCTION, t.callback)
    c.setopt(pycurl.URL, url)
    c.perform()


if __name__ == "__main__":
    if len(sys.argv) == 0:
        print "错误的参数"
    else:
        path = sys.argv[1]
        offset = sys.argv[2]
        process(path, offset)
