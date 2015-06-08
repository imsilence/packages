#!/usr/bin/env python
#encoding:utf-8

import socket

HOST, PORT = '', 43001
DATA_LENGTH = 1024

_RESPONSE = '''
HTTP/1.1 200 OK

Hello, World!
'''

def run():
    _server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    _server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    _server_socket.bind((HOST, PORT))
    _server_socket.listen(1)
    
    print 'Server Http on port %s...' % PORT

    while 1:
        _client_socket, _client_address = _server_socket.accept()
	_request = _client_socket.recv(DATA_LENGTH)

	print 'request:%s' % _request
	
	_client_socket.sendall(_RESPONSE)
	_client_socket.close()

if __name__ == '__main__':
    run()
