from http.server import BaseHTTPRequestHandler
from http import HTTPStatus

from http.client import HTTPConnection, HTTPSConnection
import shutil


class ProxyHandler(BaseHTTPRequestHandler):

    # def test_all(self):
    #     self.headers
    #     print(self.address_string())
    #     print(self.path)
    #     print(self.headers)
    #     print(self.request)


    def do_CONNECT(self):
        print("CONNECT")
        # self.test_all()
        self.send_response(HTTPStatus.OK)

    def do_GET(self):
        print("do_GET")
        # self.test_all()
        self.send_response(HTTPStatus.OK)
        conn = HTTPSConnection(self.headers.get('Host', 'ya.ru'))
        conn.request("GET", self.path)
        r1 = conn.getresponse()
        # print(r1.headers, r1.status, r1.reason)
        print(self.requestline.split()[1])
        # for k,v in r1.headers.items():
        #     print(k, v)
        #     self.send_header(k, v)
        self.end_headers()
        shutil.copyfileobj(r1, self.wfile)


    def do_POST(self):
        print("do_POST")
        return self.test_all()