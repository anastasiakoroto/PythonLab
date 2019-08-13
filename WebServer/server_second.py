from http.server import BaseHTTPRequestHandler, HTTPServer
from http.cookies import SimpleCookie
from urllib.parse import parse_qs

from read_page_inf import read_page


class ServerSecond(BaseHTTPRequestHandler):

    def do_GET(self):
        self.function_of_page[self.path](self)
        # if self.path == '/auth.html':
        #     self.authorization()
        # elif self.path == '/deauth.html':
        #     self.de_authorization()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.charge(body)

    def authorize(self):
        self.send_response(200)
        self.send_header('content-type', 'text/html')
        self.send_header('Set-Cookie', 'auth=1; HttpOnly')
        self.end_headers()
        read_page(self, 'http://localhost:8002/auth.html')

    def de_authorize(self):
        self.send_response(200)
        self.send_header('content-type', 'text/html')
        self.send_header('Set-Cookie', 'auth=0; HttpOnly')
        self.end_headers()
        read_page(self, 'http://localhost:8002/deauth.html')

    def charge(self, body):
        cookie = self.headers.get('Cookie')
        simp_cookie = SimpleCookie(cookie)
        cookie_value = simp_cookie.get('auth')
        self.send_response(200)
        self.end_headers()
        if cookie_value.value == '1':
            params = parse_qs(body.decode())
            value = params['digit'][0]
            self.wfile.write(bytes("""<br><p><center><font face="impact" size="+3" color="#93B1B4">
            OK. Peter Parker had got %s$ when he had been in London.<br> I wonder if that was enought for him...
            </font></center></p>""" % value, 'utf-8'))
            read_page(self, 'http://localhost:8002/charge.html')
        else:
            self.wfile.write(bytes('<br><p><center><font face="impact" size="+3" color="#93B1B4">'
                                   'Error. No AUTH info.</font></center></p>', 'utf-8'))
            self.wfile.write(bytes('<p><br><br><center><a href="http://localhost:8001/form.html">'
                                   '<font face="verdana" size="+2" color="#B2DDE1">BACK TO FORM'
                                   '</a><font></center><p>', 'utf-8'))

    function_of_page = {
        '/auth.html': authorize,
        '/deauth.html': de_authorize,
        '/charge.html': charge
    }


httpd = HTTPServer(('localhost', 8002), ServerSecond)
httpd.serve_forever()
