from http.server import HTTPServer
from ProxyHandler import ProxyHandler


def run(server_class=HTTPServer, handler_class=ProxyHandler):
    server_address = ('', 8080)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


if __name__ == '__main__':
    run()
