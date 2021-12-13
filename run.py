from http.server import HTTPServer, ThreadingHTTPServer
from ProxyHandler import ProxyHandler


def run(server_class=ThreadingHTTPServer, handler_class=ProxyHandler):
    server_address = ('', 8080)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


if __name__ == '__main__':
    run()
