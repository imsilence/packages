#!/usr/bin/env python
#encoding: utf-8

import logging
import threading

import time

from kazoo.client import KazooClient

_logger = logging.getLogger('zklock')

class ZKClient(KazooClient):
    
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ZKClient, cls).__new__(cls)
        return cls._instance
    
    def __init__(self, *args, **kwargs):
        super(ZKClient, self).__init__(*args, **kwargs)
        self.start()


class ZKlock(object):
    
    def __init__(self):
        self._zkclient = ZKClient(hosts='localhost:2281')
        self._lock_nameservice = '/uk/lock'
        self._lock_prefix = 'lock_id_'
        self._lock_id = ''
        self._event = threading.Event()
    
    def acquire(self, wait=True):
        if self._lock_id == '':
            self._lock_id = self._zkclient.create('%s/%s' % (self._lock_nameservice, self._lock_prefix), str(time.time()), ephemeral=True, sequence=True, makepath=True)
        
        if not self.locked():
            return True
        elif wait:
            self._event.wait()
        else:
            return False
        
    def _watch(self, *args, **kwargs):
        if not self.locked():
            self._event.set()

    
    def release(self):
        self._zkclient.exists(self._lock_id) and self._zkclient.delete(self._lock_id)
        self._lock_id = ''
        self._event.clear()
    
    def locked(self):
        if self._zkclient.exists(self._lock_nameservice):
            _children = self._zkclient.get_children(self._lock_nameservice, self._watch)
            if self._lock_id != '':
                _children.sort()
                return '%s/%s' % (self._lock_nameservice, _children[0]) != self._lock_id
            else:
                return len(_children) != 0
        else:
            return False
    
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)s %(levelname)s:%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
    _lock = ZKlock()
    for i in xrange(10):
        print _lock.acquire(True)
        print _lock.acquire(True)
        _lock.release()
    pass