#!/usr/bin/env pythonW
#encoding: utf-8

import logging
import traceback

import redis

import crypt

_logger = logging.getLogger('utils.redisclient')

class RedisClient(object):
    
    _instances = {}
    
    def __new__(cls, *args, **kwargs):
        _key = crypt.md5({'args' : args, 'kwargs' : kwargs})
        if _key not in cls._instances:
            cls._instances[_key] = super(RedisClient, cls).__new__(cls, *args, **kwargs)
            
        return cls._instances[_key]
    
    def __init__(self, host='localhost', port=6379, db=0):
        self._host = host
        self._port = port
        self._db = db
        self._connection = self._connect()
        
    def _connect(self):
        return redis.StrictRedis(host=self._host, port=self._port, db=self._db)
    
    def set(self, key, value, expire=None):
        self._connection.set(key, value, expire)
        
    def get(self, key):
        return self._connection.get(key)
    
    def push(self, key, value):
        self._connection.rpush(key, value)
        
    def pop(self, key):
        return self._connection.lpop(key)
    
    def count(self, key):
        return self._connection.llen(key)
    

class RedisObject(object):
    
    def __init__(self, key, host='localhost', port=6379, db=0):
        self._client = RedisClient(host, port, db)
        self._key = key


class RedisQueue(RedisObject):
    
    def put(self, value):
        self._client.rpush(self._key, value)
        
    def get(self):
        return self._client.lpop(self._key)
    
    def qsize(self):
        return self._client.llen(self._key)
    
    def empty(self):
        return self.qsize() == 0
    
    
class RedisString(RedisObject):
    
    def set(self, value, expire=None):
        self._client.set(self._key, value, expire)
        
    def append(self, value):
        self._client.append(self._key, value, expire)
        
    def get(self):
        return self._client.get(self._key)
    
    
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)s %(levelname)s:%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
    q1 = Queue()
    q2 = Queue()
    q1.push('test', 3)
    
    print q2.pop('test')
