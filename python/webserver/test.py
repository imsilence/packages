#!/usr/bin/env python
#encoding:utf-8

import time

def test(env, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    time.sleep(10)
    return ['time:%s' % time.time()]
