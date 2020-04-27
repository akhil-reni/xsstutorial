from __future__ import absolute_import, unicode_literals

from http.server import BaseHTTPRequestHandler
from io import BytesIO
from urllib import parse


class HTTPRequest(BaseHTTPRequestHandler):
    def __init__(self, request_text):
        self.rfile = BytesIO(request_text)
        self.raw_requestline = self.rfile.readline()
        self.error_code = self.error_message = None
        self.parse_request()

    def send_error(self, code, message):
        self.error_code = code
        self.error_message = message


class Request:
    def __init__(self):
        self.headers = None
        self.params = None
        self.data = None
        self.path = None

    def replace(self, string, payload):

        for k, v in self.headers.items():
            k.replace(string, payload)
            v.replace(string, payload)

        for k, v in self.params.items():
            self.params[k] = self.params[k].replace(string, payload)
        for k, v in self.data.items():
            self.data[k] = self.data[k].replace(string, payload)


class RequestParser(object):

    def __init__(self, request_text):
        self.request = Request()
        try:
            self.raw_request = HTTPRequest(request_text)
            if self.raw_request.error_code:
                raise Exception("failed parsing request")
            self.request.method = self.raw_request.command
            self.request.path = self.construct_path()
            self.request.headers = self.raw_request.headers
            self.request.data = self.convert(self.construct_data())
            self.request.params = self.convert(self.construct_params())
        except Exception as e:
            raise e

    def convert(self, data):
        if isinstance(data, bytes):
            return data.decode()
        if isinstance(data, (str, int)):
            return str(data)
        if isinstance(data, dict):
            return dict(map(self.convert, data.items()))
        if isinstance(data, tuple):
            return tuple(map(self.convert, data))
        if isinstance(data, list):
            return list(map(self.convert, data))
        if isinstance(data, set):
            return set(map(self.convert, data))

    def construct_path(self):
        return parse.urlsplit(self.raw_request.path).path

    def construct_data(self):
        return dict(parse.parse_qsl(self.raw_request.rfile.read(int(self.raw_request.headers.get('content-length')))))

    def construct_params(self):
        return dict(parse.parse_qsl(parse.urlsplit(self.raw_request.path).query))