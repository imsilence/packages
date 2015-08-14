#!/usr/bin/env python
#encoding: utf-8

import logging
import traceback

import pyes

import crypt

_logger = logging.getLogger('utils.esclient')

class EsClient(object):
    
    _instances = {}
    
    def __new__(cls, *args, **kwargs):
        _key = crypt.md5({'args' : args, 'kwargs' : kwargs})
        if _key not in cls._instances:
            cls._instances[_key] = super(EsClient, cls).__new__(cls)
        return cls._instances[_key]
    
    def __init__(self, hosts, timeout=10):
        self._hosts = hosts
        self._timeout = timeout
        self._connection = self._connect()
    
    def _connect(self):
        return pyes.ES(self._hosts, timeout=self._timeout)
    
    def get_connection(self):
        return self._connection
        
    def has_index(self, index):
        return self._connection.indices.exists_index(index)
    
    def create_index(self, index, settings={}):
        self._connection.indices.create_index(index, settings)
        
    def delete_index(self, index):
        self._connection.indices.delete_index(index)
        
    def has_doctype(self, index, doctype):
        if self.has_index(index):
            _mapping = self._connection.indices.get_mapping(indices=index)
            # _mapping.get_doctype has bug
            _doctypes = _mapping.get_doctypes(index)
            return doctype in dict(_doctypes)
        
        return False

    def create_doctype(self, index, doctype, mapping):
        if not self.has_index(index):
            self.create_index(index)
        self._connection.indices.put_mapping(doctype, {'properties' : mapping}, index)
        

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)s %(levelname)s:%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
        
    c = EsClient(['localhost:9200'])
    
    c.create_doctype('config', 'alarm1', {'test' : {'type' : 'long'}})
    
