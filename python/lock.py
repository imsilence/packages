#!/usr/bin/env python
#encoding: utf-8

import os
import time
import random

from fileutils import read_file, write_file, delete_file

_PATH_ = os.path.normpath(os.path.dirname(os.path.abspath(__file__)))

class Lock(object):
    pass

class FileLock(object):
    
    def __init__(self, path='', expires=0):
        self._path = path or os.path.join(_PATH_, 'lock_%s_%s.lock' % (int(time.time() * 1000), random.randint(0, 10000)))
        self._expires = expires
        print self._path
    
    def acquire(self):
        if not self.locked():
            write_file(self._path, time.time())
            return True
            
        return False
    
    def relese(self):
        delete_file(self._path)
    
    def locked(self):
        if os.path.exists(self._path):
            _cxt = read_file(self._path)
            _time = 0 if _cxt == '' else float(_cxt)
            return (not not _time) if self._expires == 0 else (time.time() <= _time + self._expires) 
        
        return False
        

if __name__ == '__main__':
    _lock = FileLock(path='e:/test.txt', expires=5)
    print 'status:', _lock.locked()
    print 'acquire:', _lock.acquire()
    for i in xrange(8):
        print 'status:', _lock.locked()
        print 'acquire:', _lock.acquire()
        time.sleep(1)
     
    print 'status:', _lock.locked()
    print 'acquire:', _lock.acquire()
    _lock.relese()
    print 'status:', _lock.locked()
    print 'acquire:', _lock.acquire()
    print 'status:', _lock.locked()
    _lock.relese()
