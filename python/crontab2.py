#!/usr/bin/env python
#encoding: utf-8

import os
import logging
import traceback
import time
import datetime

from cmdutils import exec_cmd

_logger = logging.getLogger('crontab')

_config_paths = ['./scripts/crontab']

def read_configs():
    _commands = []
    for _path in _config_paths:
        _path = os.path.abspath(_path)
        if not os.path.exists(_path):
            logger.error('crontab config file not exists, path:%s', _path)
            continue
        
        _cwd = os.path.dirname(_path)
        with open(_path, 'rb') as _handler:
            for _line in _handler:
                _line = _line.strip()
                
                if _line == '' or _line.startswith('#'):
                    continue
                
                _sp = _line.split()
                
                if len(_sp) < 6:
                    _logger.error('crontab file config error, path:%s, line:%s', _path, _line)
                _commands.append({'time_sequence': _sp[:5], 'cmd': _sp[5:], 'cwd': _cwd})
    return _commands

def _judge_time(current_time_sequence, _time_sequence):
    for _i in xrange(5):
        if _time_sequence[_i] == '*':
            continue
        elif str(_time_sequence[_i]).startswith('*/'):
            if int(current_time_sequence[_i]) % int(str(_time_sequence[_i])[2:]) != 0:
                return False
        else:
            if int(_time_sequence[_i]) != int(current_time_sequence[_i]): 
                return False
    
    return True

def _execute_cmd(cmd, cwd):
    return exec_cmd(cmd, cwd=cwd)[0]

def _judge_execute_commands(current_time, commands):
    _current_datetime = datetime.datetime.fromtimestamp(current_time)
    _current_time_sequence = [_current_datetime.minute, _current_datetime.hour, _current_datetime.day, _current_datetime.month, (_current_datetime.weekday()) + 1 % 7]
    for _command in commands:
        _time_sequence = _command.get('time_sequence')
        if _judge_time(_current_time_sequence, _time_sequence):
            _cmd = _command.get('cmd')
            _cwd = _command.get('cwd')
            _code = _execute_cmd(_cmd, _cwd)
            _logger.debug('execute cmd: %s, result:%s', _cmd, _code)


TIMESLEEP = 3
INTERVAL_MINUTE = 60

_next_time = 0
_commands = read_configs()

def crontab():
    global _next_time
    _current_time = time.time()
    if _current_time >= _next_time:
        _logger.debug('judge exec commands')
        _judge_execute_commands(_current_time, _commands)
        _next_time = _current_time + INTERVAL_MINUTE
        

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)s %(levelname)s:%(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        )
    crontab()
