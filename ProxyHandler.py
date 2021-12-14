from http.server import BaseHTTPRequestHandler
from http import HTTPStatus
from http.client import HTTPSConnection
from utils import add_tm
import shutil


class ProxyHandler(BaseHTTPRequestHandler):
    """HTTP request handler proxy class.

    Proxy request to news.ycombinator.com and add tm-symbol to 6-words
    """

    def do_GET(self):
        con = HTTPSConnection('news.ycombinator.com')
        con.request(self.command, self.path)
        response = con.getresponse()
        self.send_response(HTTPStatus.OK)
        self.end_headers()
        if response.headers.get('Content-Type', None) == 'text/html; charset=utf-8':
            # For html-files add tm-symbol
            data = add_tm(response)
            self.wfile.write(data)
        else:
            # For others send original answer
            shutil.copyfileobj(response, self.wfile)
        con.close()
