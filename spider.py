#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
socket.setdefaulttimeout(10)
import sys
import re
import urllib

from thread_pool import ThreadPool
from common import GLOBAL_CONFIG

class Spider(object):
    def __init__(self, url, depth=1):
        self.url = url
        self.depth = depth
        self.depth_flg = 1

    def spider(self, id, sleep = 0.001):
        try:
            html = urllib.urlopen(self.url).read()
            self.get_page_url(html)
            ret = "success!"
        except:
            print sys.exc_info()
            ret = "error!!!"
        return ret

    def get_page_url(self, html):
        re_url = re.compile(r'<a.*?href=.*?<\/a>')
        urls = re_url.findall(html)

def test_job(id, sleep = 0.001):
    try:
        urllib.urlopen(GLOBAL_CONFIG.get('url', {}).get('url')).read()
        ret = "success"
    except:
        #print '%4d'%id, sys.exc_info()
        ret = "error"

    return ret

def test():
    print 'start testing'
    wm = ThreadPool(10)
    for i in range(1):
        wm.add_job(test_job, i, i*0.001)
    wm.wait_for_complete()
    print 'end testing'

test()
