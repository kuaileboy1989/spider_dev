#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Queue
import sys
from threading import Thread
import time
import urllib

class MyThread(Thread):
    def __init__(self, workQueue, resultQueue, t_id, timeout=0, **kwds):
        Thread.__init__(self, **kwds)
        self.id = t_id
        self.setDaemon(True)
        self.workQueue = workQueue
        self.resultQueue = resultQueue
        self.timeout = timeout
        self.start()

    def run(self):
        while True:
            try:
                callback, args, kwds = self.workQueue.get(timeout=self.timeout)
                res = callback(*args, **kwds)
                print "worker[%2d]: %s"%(self.id, str(res))
                self.resultQueue.put(res)
            except Queue.Empty:
                break
            except:
                print 'worker[%2d]'%self.id, sys.exc_info()[:2]

class ThreadPool(object):
    def __init__(self, num_of_workers=10, timeout=1):
        self.workQueue = Queue.Queue()
        self.resultQueue = Queue.Queue()
        self.workers = []
        self.timeout = timeout
        self._recruitThreads(num_of_workers)

    def _recruitThreads(self, num_of_workers):
        for i in range(num_of_workers):
            worker = MyThread(self.workQueue, self.resultQueue, i, self.timeout)
            self.workers.append(worker)

    def wait_for_complete(self):
        while len(self.workers):
            worker = self.workers.pop()
            worker.join()
            if worker.isAlive() and not self.workQueue.empty():
                self.workers.append(worker)
        print "All jobs are completed."

    def add_job(self, callable, *args, **kwds):
        self.workQueue.put((callable, args, kwds))

    def get_result(self, *args, **kwds):
        return self.resultQueue.get(*args, **kwds)
'''
def test_job(id, sleep = 0.001):
    try:
        urllib.urlopen('[url]http://www.baidu.com[/url]').read()
    except:
        print '%4d'%id, sys.exc_info()[:2]

def test():
    import socket
    socket.setdefaulttimeout(10)
    print 'start testing'
    wm = ThreadPool(10)
    for i in range(10):
        wm.add_job(test_job, i, i*0.001)
    wm.wait_for_complete()
    print 'end testing'

test()
'''
