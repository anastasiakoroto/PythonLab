from http.server import BaseHTTPRequestHandler, HTTPServer
from http.cookies import SimpleCookie
from urllib.parse import parse_qs


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
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.charge(body)

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
        title = '<p><font color="#B2DDE1" face="impact" size="+3">form page</font></p>'

        auth_condition = (cookie_value is None or cookie_value.value == '0')
        context_dict = {'title': head_title,
                        'page_title': title,
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

    def charge(self, body):
        cookie = self.headers.get('Cookie')
        simp_cookie = SimpleCookie(cookie)
        cookie_value = simp_cookie.get('auth')
        back_to_form = True
        if cookie_value is None or cookie_value.value == '0':
            error_message = 'Unauthorized'
            error_dict = {'title': 'ERROR',
                          'error_status': 401,
                          'message': error_message,
                          'back_to_form': back_to_form,
                          'server_one_host': SERVERS_HOST,
                          'server_one_port': SERVER_ONE_PORT}
            page = read_page('/error.html', **error_dict)
            response = 401
        else:
            params = parse_qs(body.decode())
            if params.get('digit') is not None:
                value = params['digit'][0]
                context_dict = {'title': 'RESPONSE',
                                'value': value,
                                'server_one_host': SERVERS_HOST,
                                'server_one_port': SERVER_ONE_PORT}
                page = read_page('/charge.html', **context_dict)
                response = 200
            else:
                error_message = 'The form is filled out incorrectly'
                error_dict = {'title': 'ERROR',
                              'error_status': 400,
                              'message': error_message,
                              'back_to_form': back_to_form,
                              'server_one_host': SERVERS_HOST,
                              'server_one_port': SERVER_ONE_PORT}
                page = read_page('/error.html', **error_dict)
                response = 400
        self.send_response(response)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(page)

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
        print('Shutting down server.')
