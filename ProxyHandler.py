from http.server import BaseHTTPRequestHandler
from http import HTTPStatus
from http.client import HTTPSConnection
from utils import rebuild_page
import shutil


class ProxyHandler(BaseHTTPRequestHandler):
    """HTTP request handler proxy class.

    Proxy request to news.ycombinator.com and add tm-symbol to 6-words
    """
    ACCEPTABLE_RESPONSE_HEADERS = [
        'Cache-Control',
        'Content-Type',
        # 'Content-Encoding', TODO: Decide what to do with different encodings 4exmpl gzip
        'Vary',
        'Referrer-Policy',
        'Set-Cookie',
        'Location',
    ]

    ACCEPTABLE_REQUEST_HEADERS = [
        'Cache-Control',
        'Content-Type',
        'Content-Length',
        'Accept',
        'User-Agent',
        # 'Accept-Encoding', # TODO: Decide what to do with different encodings 4exmpl gzip
        'Accept-Language',
        'Cookie',
    ]

    def do_GET(self):
        con = HTTPSConnection('news.ycombinator.com')
        headers = {k: v for k, v in self.headers.items() if k in self.ACCEPTABLE_REQUEST_HEADERS}
        con.request(self.command, self.path, headers=headers)
        response = con.getresponse()
        self.send_response(response.status)
        for k,v in response.headers.items():
            if k in self.ACCEPTABLE_RESPONSE_HEADERS:
                self.send_header(k, v)
        self.end_headers()
        if response.status == HTTPStatus.OK:
            if response.headers.get('Content-Type', None) == 'text/html; charset=utf-8':
                # For html-files add tm-symbol
                data = rebuild_page(response)
                self.wfile.write(data)
            else:
                # For others send original answer
                shutil.copyfileobj(response, self.wfile)
        con.close()


    def do_POST(self):
        con = HTTPSConnection('news.ycombinator.com')
        headers = {k: v for k, v in self.headers.items() if k in self.ACCEPTABLE_REQUEST_HEADERS}
        body_str = self.rfile.read(int(self.headers.get('Content-Length', '0')))
        con.request(self.command, self.path, body=body_str, headers=headers)
        response = con.getresponse()
        self.send_response(response.status)
        print(response.headers)
        for k,v in response.headers.items():
            if k in self.ACCEPTABLE_RESPONSE_HEADERS:
                self.send_header(k, v)
        self.end_headers()

        if response.status == HTTPStatus.OK:
            if response.headers.get('Content-Type', None) == 'text/html; charset=utf-8':
                # For html-files add tm-symbol
                data = rebuild_page(response)
                self.wfile.write(data)
            else:
                # For others send original answer
                shutil.copyfileobj(response, self.wfile)
        con.close()

