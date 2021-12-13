from http.server import BaseHTTPRequestHandler
from http import HTTPStatus
from http.client import HTTPConnection, HTTPSConnection
import shutil


class ProxyHandler(BaseHTTPRequestHandler):
    pass