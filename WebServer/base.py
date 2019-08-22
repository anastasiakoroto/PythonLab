from http.server import BaseHTTPRequestHandler, HTTPServer
from http.cookies import SimpleCookie
import cgi

from read_page_inf import read_page
from error_handler import not_found_page
from const import SERVERS_HOST, SERVER_ONE_PORT, SERVER_TWO_PORT


class BaseServer(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            self.function_of_page[self.path](self)
        except KeyError:
            not_found_page(self)

    def do_POST(self):
        self.charge()

    def do_OPTIONS(self):
        self.send_response(200, 'ok')
        self.send_header('Content-Type', 'text/html')
        self.send_cors_headers()
        self.end_headers()

    def send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", 'http://localhost:8001')
        self.send_header("Access-Control-Allow-Credentials", 'true')
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Method", "GET, POST, OPTIONS")

    def hello_page(self):
        page = read_page('/hello_page.html', server_one_host=SERVERS_HOST, server_one_port=SERVER_ONE_PORT)
        self.send_response(200)
        self.send_header('content-type', 'text/html')
        self.end_headers()
        self.wfile.write(page)

    def form(self):
        cookie = self.headers.get('Cookie')
        simple_cookie = SimpleCookie(cookie)
        cookie_value = simple_cookie.get('auth')
        head_title = 'FORM'
        auth_condition = (cookie_value is None or cookie_value.value == '0')
        context_dict = {'title': head_title,
                        'auth_condition': auth_condition,
                        'server_two_host': SERVERS_HOST,
                        'server_two_port': SERVER_TWO_PORT,
                        'server_one_port': SERVER_ONE_PORT}
        page = read_page('/form.html', **context_dict)
        self.send_response(200)
        self.send_header('content-type', 'text/html')
        self.end_headers()
        self.wfile.write(page)

    def authorize(self):
        context_dict = {'title': 'AUTH', 'server_one_host': SERVERS_HOST, 'server_one_port': SERVER_ONE_PORT}
        page = read_page('/auth.html', **context_dict)
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.send_header('Set-Cookie', 'auth=1; HttpOnly')
        self.end_headers()
        self.wfile.write(page)

    def de_authorize(self):
        context_dict = {'title': 'de-AUTH', 'server_one_host': SERVERS_HOST, 'server_one_port': SERVER_ONE_PORT}
        page = read_page('/deauth.html', **context_dict)
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.send_header('Set-Cookie', 'auth=0; HttpOnly')
        self.end_headers()
        self.wfile.write(page)

    def charge(s):
        cookie = s.headers.get('Cookie')
        simp_cookie = SimpleCookie(cookie)
        cookie_value = simp_cookie.get('auth')
        if cookie_value is None or cookie_value.value == '0':
            alert_message = '401 error: Unauthorized'
            response = 401
        else:
            post_form = cgi.FieldStorage(
                fp=s.rfile,
                headers=s.headers,
                environ={'REQUEST_METHOD': 'POST',
                         'CONTENT_TYPE': s.headers['Content-Type']
                         })
            value = post_form.getvalue('digit')
            if value != '':
                alert_message = f'OK. Peter Parker had got { value }$ when he had been in London. I wonder if that ' \
                                f'was enough for him...'
                response = 200
            else:
                alert_message = '400 error: The form is filled out incorrectly'
                response = 400
        s.send_response(response)
        s.send_cors_headers()
        s.send_header('Content-Type', 'text/html')
        s.end_headers()
        s.wfile.write(alert_message.encode('utf-8'))

    function_of_page = {
        '/': hello_page,
        '/hello_page.html': hello_page,
        '/auth.html': authorize,
        '/deauth.html': de_authorize,
        '/form.html': form
    }


def run(server_host, port_number, server_name):
    httpd = HTTPServer((server_host, port_number), server_name)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('Program closed.')
