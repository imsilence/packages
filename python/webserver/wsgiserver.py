#!/usr/bin/env python
#encoding:utf-8

import socket
import StringIO
import sys


class WSGIServer(object):
    
    address_family = socket.AF_INET
    socket_type = socket.SOCK_STREAM
    request_queue_size = 1
    recv_size = 1024

    def __init__(self, server_address):
        self._listen_socket = _listen_socket = socket.socket( \
	    self.address_family,
	    self.socket_type)
	_listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	_listen_socket.bind(server_address)
	_listen_socket.listen(self.request_queue_size)
	_host, _port = _listen_socket.getsockname()
	self._server_name = socket.getfqdn(_host)
	self._server_port = _port
	self._headers_set = []
	self._application = None
	self._client = None
	self._request_data = None
	self._request_method = None
	self._path = None
	self._request_version = None
	self._start_response = None

    def set_application(self, application):
        self._application = application

    def server_forever(self):
        _listen_socket = self._listen_socket
	while 1:
	    self._client, _addr = _listen_socket.accept()
	    self._handle_request()

    def _handle_request(self):
        self._request_data = _request_data = self._client.recv(self.recv_size)
	self._parse_request_data(_request_data)
	_env = self._get_environment()
	_result = self._application(_env, self.start_response)
	self._finish_response(_result)

    def _parse_request_data(self, request_data):
        _request_line = str(request_data.splitlines()[0]).rstrip('\r\n')
	(self._request_method, self._path, self._request_version) = _request_line.split()

    def _get_environment(self):
        _env = {}
	_env['wsgi.version'] = (1, 0)
	_env['wsgi.url_scheme'] = 'http'
	_env['wsgi.input'] = StringIO.StringIO(self._request_data)
	_env['wsgi.errors'] = sys.stderr
	_env['wsgi.multithread'] = False
	_env['wsgi.multiprocess'] = False
	_env['wsgi.run_once'] = False
	_env['REQUEST_METHOD'] = self._request_method.upper()
	_env['PATH_INFO'] = self._path
	_env['SERVER_NAME'] = self._server_name
	_env['SERVER_PORT'] = self._server_port
        return _env

    def start_response(self, status, response_headers, exc_info=None):
        _server_headers = [
	    ('Date', 'Sun, 7 Jun 2015 23:07:04 GMT'),
	    ('Server', 'WSGIServer 0.1')
	    ]
	self._headers_set = [status, response_headers + _server_headers]

    def _finish_response(self, result):
        _status, _response_headers = self._headers_set
	_response = 'HTTP/1.1 {status}\r\n'.format(status=_status)
	for _header in _response_headers:
	    _response += '{0}:{1}\r\n'.format(*_header)
	_response += '\r\n'
	for _data in result:
	    _response += _data
	self._client.sendall(_response)
	self._client.close()


def make_server(server_address, application):
    server = WSGIServer(server_address)
    server.set_application(application)
    return server

SERVER_ADDRESS = ('localhost', 43001)

if __name__ == '__main__':
    app_path = sys.argv[1]
    module, application = app_path.split(':')
    module = __import__(module)
    application = getattr(module, application)
    httpd = make_server(SERVER_ADDRESS, application)
    httpd.server_forever()


