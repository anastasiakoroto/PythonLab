from http.server import BaseHTTPRequestHandler, HTTPServer
from http.cookies import SimpleCookie

from read_page_inf import read_page


class ServerFirst(BaseHTTPRequestHandler):

    def do_GET(self):
        page_name = self.path
        self.function_of_page[page_name](self)
        # if self.path == '/' or self.path == '/hello_page.html':
        #     self.hello_page()
        # elif self.path == '/form.html':
        #     self.form()

    def hello_page(self):
        self.send_response(200)
        self.send_header('content-type', 'text/html')
        self.end_headers()
        read_page(self, 'http://localhost:8001/hello_page.html')

    def form(self):
        self.send_response(200)
        self.send_header('content-type', 'text/html')
        self.end_headers()
        cookie = self.headers.get('Cookie')
        simp_cookie = SimpleCookie(cookie)
        cookie_value = simp_cookie.get('auth')
        self.wfile.write(bytes('<p><font color="#B2DDE1" face="impact" size="+3">form page</font></p>', 'utf-8'))
        if cookie_value.value == '0' or cookie_value is None:
            authorize_page = '<p><a href="http://localhost:8002/auth.html"><font color="#899597" size="+1" ' \
                             'face="verdana">AUTHORIZE</font></a></p>'
            self.wfile.write(bytes(authorize_page, 'utf-8'))
            read_page(self, 'http://localhost:8001/form.html')
        else:
            de_authorize_page = '<p><a href="http://localhost:8002/deauth.html"><font color="#899597" size="+1" ' \
                                'face="verdana">DE-AUTHORIZE</font></a></p>'
            self.wfile.write(bytes(de_authorize_page, 'utf-8'))
            read_page(self, 'http://localhost:8001/form.html')

    function_of_page = {
        '/': hello_page,
        '/hello_page.html': hello_page,
        '/form.html': form
    }


httpd = HTTPServer(('localhost', 8001), ServerFirst)
httpd.serve_forever()
