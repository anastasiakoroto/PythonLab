from http.server import BaseHTTPRequestHandler, HTTPServer
from http.cookies import SimpleCookie
from urllib.parse import parse_qs

from read_page_inf import read_page
from error_handler import not_found_page


class ServerTwo(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            self.function_of_page[self.path](self)
        except KeyError:
            not_found_page(self, self.path)

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.charge(body)

    def authorize(self):
        response, page = read_page('/auth.html')
        self.send_response(response)
        self.send_header('content-type', 'text/html')
        self.send_header('Set-Cookie', 'auth=1; HttpOnly')
        self.end_headers()
        self.wfile.write(page.encode('utf-8'))

    def de_authorize(self):
        response, page = read_page('/deauth.html')
        self.send_response(response)
        self.send_header('content-type', 'text/html')
        self.send_header('Set-Cookie', 'auth=0; HttpOnly')
        self.end_headers()
        self.wfile.write(page.encode('utf-8'))

    def charge(s, body):
        cookie = s.headers.get('Cookie')
        simp_cookie = SimpleCookie(cookie)
        cookie_value = simp_cookie.get('auth')
        back_to_form_button = '<p><a href="http://localhost:8001/form.html"><font size="+2" face="impact" ' \
                              'color="ACCACD">BACK TO FORM</font></a></p>'
        if cookie_value is None or cookie_value.value == '0':
            error_message = '<br />Unauthorized'
            _, page = read_page('/error.html', error_status=401, message=error_message,
                                back_to_form=back_to_form_button)
            response = 401
        else:
            params = parse_qs(body.decode())
            if params.get('digit') is not None:
                value = params['digit'][0]
                message = f"""<br/><p><center><font face="impact" size="+3" color="#93B1B4"> OK. Peter Parker had got 
                {value}$ when he had been in London.<br /> I wonder if that was enough for him...</font></center></p>"""
                response, page = read_page('/charge.html', message=message)
            else:
                error_message = '<br />The form is filled out incorrectly'
                _, page = read_page('/error.html', error_status=400, message=error_message,
                                    back_to_form=back_to_form_button)
                response = 400
        s.send_response(response)
        s.send_header('content-type', 'text/html')
        s.end_headers()
        s.wfile.write(page.encode('utf-8'))

    function_of_page = {
        '/auth.html': authorize,
        '/deauth.html': de_authorize
    }


httpd = HTTPServer(('localhost', 8002), ServerTwo)
httpd.serve_forever()
