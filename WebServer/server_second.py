from http.server import BaseHTTPRequestHandler, HTTPServer
from http.cookies import SimpleCookie
from urllib.parse import parse_qs

from read_page_inf import read_page
from error_handler import error_page


class ServerSecond(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path in self.function_of_page:
            self.function_of_page[self.path](self)
        else:
            error_page(self, self.path)

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.charge(body)

    def authorize(self):
        response, page = read_page('http://localhost:8002/auth.html')
        self.send_response(response)
        self.send_header('content-type', 'text/html')
        self.send_header('Set-Cookie', 'auth=1; HttpOnly')
        self.end_headers()
        self.wfile.write(page.encode('utf-8'))

    def de_authorize(self):
        response, page = read_page('http://localhost:8002/deauth.html')
        self.send_response(response)
        self.send_header('content-type', 'text/html')
        self.send_header('Set-Cookie', 'auth=0; HttpOnly')
        self.end_headers()
        self.wfile.write(page.encode('utf-8'))

    def charge(s, body):
        cookie = s.headers.get('Cookie')
        simp_cookie = SimpleCookie(cookie)
        cookie_value = simp_cookie.get('auth')
        if cookie_value is None or cookie_value.value == '0':
            auth_message = """<br /><p><center><font face="impact" size="+3" color="#93B1B4">
            Error. No AUTH info.</font></center></p>"""
            response, page = read_page('http://localhost:8002/charge.html', message=auth_message)
        else:
            params = parse_qs(body.decode())
            if len(params) > 0:
                value = params['digit'][0]
                message = f"""<br/><p><center><font face="impact" size="+3" color="#93B1B4"> OK. Peter Parker 
                had got {value}$ when he had been in London.<br /> I wonder if that was enough for him...</font>
                </center></p>"""
                response, page = read_page('http://localhost:8002/charge.html', message=message)
            else:
                response, page = read_page('http://localhost:8002/error.html')
                response = 404
        s.send_response(response)
        s.send_header('content-type', 'text/html')
        s.end_headers()
        s.wfile.write(page.encode('utf-8'))

    function_of_page = {
        '/auth.html': authorize,
        '/deauth.html': de_authorize
    }


httpd = HTTPServer(('localhost', 8002), ServerSecond)
httpd.serve_forever()
