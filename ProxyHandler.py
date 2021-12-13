from http.server import BaseHTTPRequestHandler
from http import HTTPStatus
from http.client import HTTPSConnection
import shutil


class ProxyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        con = HTTPSConnection('news.ycombinator.com')
        con.request("GET", self.path)
        response = con.getresponse()
        self.send_response(HTTPStatus.OK)
        self.end_headers()
        shutil.copyfileobj(response, self.wfile)

    def do_POST(self):
        self.send_response(HTTPStatus.OK)