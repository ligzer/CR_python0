from http.server import BaseHTTPRequestHandler
from http import HTTPStatus
from http.client import HTTPConnection, HTTPSConnection
import shutil


class ProxyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(HTTPStatus.OK)

    def do_POST(self):
        self.send_response(HTTPStatus.OK)