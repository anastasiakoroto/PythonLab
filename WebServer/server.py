from http.server import BaseHTTPRequestHandler, HTTPServer

import pages_response


class Server(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path in pages_response.function_of_page:
            pages_response.function_of_page[self.path](self)
        else:
            pages_response.error_page(self)

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        pages_response.charge(self, body)


httpd = HTTPServer(('localhost', 8001), Server)
httpd.serve_forever()
