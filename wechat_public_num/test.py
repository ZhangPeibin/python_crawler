#!/usr/bin/env python
# -*- coding: utf-8 -*-
import wechatsogou
import json
import time
for i in range(1000):
    ws_api =wechatsogou.WechatSogouAPI()
    u = ws_api.get_gzh_info('阿里技术')
    print json.dumps(u, encoding="UTF-8", ensure_ascii=False)
    time.sleep(3)