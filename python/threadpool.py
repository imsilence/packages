#!/usr/bin/env python
#encoding: utf-8

import logging
import traceback
import threading
import Queue
import time

_logger = logging.getLogger('')

class SelfException(Exception):
    pass

class Task(object):
    
    def __init__(self, callback, *args, **kwargs):
        self._callback = callback
        self._args = args
        self._kwargs = kwargs
    
    def dispose(self):
        self._callback(*self._args, **self._kwargs)
        
class Worker(threading.Thread):
    
    def __init__(self, pool):
        super(Worker, self).__init__()
        self._id =  pool.get_worker_id()
        self.setName('Worker#%s' % self._id)
        self.setDaemon(True)
        self._pool = pool
        self._dispose = False
        self._busy = False
    
    def get_id(self):
        return self._id
    
    def is_busy(self):
        return self._busy
    
    def is_dispose(self):
        return self._dispose
    
    def dispose(self):
        self._dispose = True
    
    def run(self):
        while not self._dispose:
            _task = self._pool.get_task()
            if _task is not None:
                self._busy = True
                _task.dispose()
                self._busy = False
            time.sleep(0.1)


class ThreadPool(object):
    
    def __init__(self, min_size=3):
        self._min_size = min_size
        self._max_size = min_size
        self._task_queue = Queue.Queue()
        self._workers = {}
        self._worker_count = 0
        self._idx = 0
        self._init_workers()
    
    def get_worker_id(self):
        self._idx += 1
        return self._idx
    
    def _init_workers(self):
        for _i in xrange(self._min_size):
            self._add_worker()
        
    def _add_worker(self):
        if self._worker_count < self._max_size:
            _worker = Worker(self)
            _worker.start()
            self._workers[_worker.get_id()] = _worker
            self._worker_count += 1
    
    def add_task(self, task):
        if not isinstance(task, Task):
            raise SelfException('Parameters must be inherited from type object Callback')
        self._task_queue.put(task)
    
    def add_tasks(self, tasks):
        for task in tasks:
            self.add_task(task, False)
            
    def get_task(self):
        return self._task_queue.get()
    
    def get_size(self):
        return self._task_queue.qsize()
            

if __name__ == '__main__':
    
    def test(*args, **kwargs):
        print kwargs['i']
    
    _pool = ThreadPool()
    for i in xrange(9):
        _pool.add_task(Task(test, i=i))
    while True:
        _size = _pool.get_size()
        if _size == 0:
            time.sleep(5)
            for i in xrange(9):
                _pool.add_task(Task(test, i=i))
        time.sleep(1)
        
    pass