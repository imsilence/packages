#!/usr/bin/env python
#encoding: utf-8

import os
import logging
import subprocess

_logger = logging.getLogger('utils.cmdutils')

def exec_cmd(args, async=False, cwd=None):
   return _async_exec_cmd(args, cwd) if async else _sync_exec_cmd(args, cwd)


def _async_exec_cmd(args, cwd=None):
    _cmd = []

    if cwd is not None:
        _cmd.append('cd /d "%s"' % cwd)
        _cmd.append('&&')

    if os.name == 'nt':
        _cmd.append('start')

    _cmd += args if isinstance(args, list) else [args]
   
    _returncode = os.system(' '.join(_cmd))

    _returncode = 0
    _output = ''
    _pid = -1

    _logger.debug('async exec cmd: %s, returncode, %d, output:%s, pid:%d', _cmd, _returncode, _output, _pid)
    return [_returncode, _output, _pid]


def _sync_exec_cmd(args, cwd=None):
    startupinfo = None
    if os.name == 'nt':
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE

    _process = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False, cwd=cwd)
    _stdout, _stderr = _process.communicate()
    _returncode = _process.returncode
    _pid = _process.pid
    _output = ''
    try:
        _output = str(_stdout)
    except BaseException:
        pass
    _logger.debug('sync exec cmd: %s, returncode, %d, output:%s, pid:%d', args, _returncode, _output, _pid)
    return [_returncode, _output, _pid]
    
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)s %(levelname)s:%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
    print exec_cmd(['python', 'test.py'], True, cwd=r"d:\\")
    print exec_cmd(['ping ', 'www.360.cn', '-n 100'], True, cwd=r"d:\\")
    print exec_cmd(['ping ', 'www.360.cn'])
    