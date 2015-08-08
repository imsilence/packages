#!/usr/bin/env ptyhon
#encoding: utf-8
import logging
import traceback
import threading
import time

_logger = logging.getLogger('utils.runserver')

_RUNNING = True

NIL = lambda *args, **kwargs: None

class SelfException(Exception):
    pass

class Callback(object):
    
    def __init__(self, **kwargs):
        self.init = kwargs.get('init', NIL)
        self.callback = kwargs.get('callback', NIL)
        self.dispose = kwargs.get('dispose', NIL)
        self.timesleep = float(kwargs.get('timesleep', 1))
    

class DaemonThread(threading.Thread):
    
    def __init__(self, callback, timesleep=1):
        super(DaemonThread, self).__init__()
        self.setName('thread_daemon')
        self.setDaemon(True)
        self._callback = callback
        self._timesleep = timesleep
        
    def run(self):
        _callback = self._callback
        while 1:
            try:
                _callback()
            except BaseException:
                _logger.exception(traceback.format_exc())
            finally:
                time.sleep(self._timesleep)

def run_as_server(callbacks, timesleep=0.5):
    if not isinstance(callbacks, list):
        callbacks = [callbacks]
        
    _disponse_funcs = []
    try:
        for _callback in callbacks:
            if not isinstance(_callback, Callback):
                raise SelfException('Parameters must be inherited from type object Callback')
        
            _init_func = getattr(_callback, 'init')
            _callback_func = getattr(_callback, 'callback')
            _dispose_func = getattr(_callback, 'dispose')
            _timesleep = getattr(_callback, 'timesleep')
            
            _init_func()
            DaemonThread(_callback_func, _timesleep).start()
            
            _disponse_funcs.append(_dispose_func)
            
        while _RUNNING:
            time.sleep(1)
    except BaseException:
        _logger.exception(traceback.format_exc())
    finally:
        for _dispose_func in _disponse_funcs:
            _dispose_func()
            
def stop_server():
    global _RUNNING
    _RUNNING = False

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)s %(levelname)s:%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
    def callback1():
        print 'callback1:', time.time()
        
    def callback2():
        pass
        
    def stop():
        time.sleep(1000)
        stop_server()
        
    threading.Thread(target=stop).start()
    run_as_server([Callback(callback=callback1),Callback(callback=callback2)])
