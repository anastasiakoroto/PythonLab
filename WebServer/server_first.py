from http.server import BaseHTTPRequestHandler, HTTPServer
from http.cookies import SimpleCookie

from read_page_inf import read_page
from error_handler import error_page


class ServerFirst(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path in self.function_of_page:
            self.function_of_page[self.path](self)
        else:
            error_page(self, self.path)

    def hello_page(self):
        response, page = read_page('http://localhost:8001/hello_page.html')
        self.send_response(response)
        self.send_header('content-type', 'text/html')
        self.end_headers()
        self.wfile.write(page.encode('utf-8'))

    def form(self):
        cookie = self.headers.get('Cookie')
        simple_cookie = SimpleCookie(cookie)
        cookie_value = simple_cookie.get('auth')
        title = '<p><font color="#B2DDE1" face="impact" size="+3">form page</font></p>'
        if cookie_value is None or cookie_value.value == '0':
            auth_page = '<p><a href="http://localhost:8002/auth.html"><font color="#899597" size="+1" face="verdana">' \
                        'AUTHORIZE</font></a></p>'
            response, page = read_page('http://localhost:8001/form.html', page_title=title, auth_page=auth_page)
        else:
            de_auth_page = '<p><a href="http://localhost:8002/deauth.html"><font color="#899597" size="+1" ' \
                           'face="verdana">DE-AUTHORIZE</font></a></p>'
            response, page = read_page('http://localhost:8001/form.html', page_title=title, auth_page=de_auth_page)
        self.send_response(response)
        self.send_header('content-type', 'text/html')
        self.end_headers()
        self.wfile.write(page.encode('utf-8'))

    function_of_page = {
        '/': hello_page,
        '/hello_page.html': hello_page,
        '/form.html': form
    }


httpd = HTTPServer(('localhost', 8001), ServerFirst)
httpd.serve_forever()