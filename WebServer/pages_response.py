from http.cookies import SimpleCookie
from urllib.parse import parse_qs


def read_page(s, s_path):
    try:
        page_to_open = open(s_path[1:], 'r').read()
    except OSError:
        s.send_response(404)
        page_to_open = open('error.html', 'r').read()
    s.wfile.write(bytes(page_to_open, 'utf-8'))


def hello_page(s):
    s.send_response(200)
    s.send_header('content-type', 'text/html')
    s.end_headers()
    read_page(s, '/hello_page.html')


def authorize(s):
    s.send_response(200)
    s.send_header('content-type', 'text/html')
    s.send_header('Set-Cookie', 'auth=1; HttpOnly')
    s.end_headers()
    read_page(s, '/auth.html')


def de_authorize(s):
    s.send_response(200)
    s.send_header('content-type', 'text/html')
    s.send_header('Set-Cookie', 'auth=0; HttpOnly')
    s.end_headers()
    read_page(s, '/deauth.html')


def form(s):
    s.send_response(200)
    s.send_header('content-type', 'text/html')
    s.end_headers()
    cookie = s.headers.get('Cookie')
    simple_cookie = SimpleCookie(cookie)
    cookie_value = simple_cookie.get('auth')
    s.wfile.write(bytes('<p><font color="#B2DDE1" face="impact" size="+3">form page</font></p>', 'utf-8'))
    if cookie_value.value == '0' or cookie_value is None:
        auth_page = '<p><a href="/auth.html"><font color="#899597" size="+1" face="verdana">AUTHORIZE</font></a></p>'
        s.wfile.write(bytes(auth_page, 'utf-8'))
        read_page(s, '/form.html')
    else:
        de_auth_page = '<p><a href="/deauth.html"><font color="#899597" size="+1" face="verdana">DE-AUTHORIZE' \
                       '</font></a></p>'
        s.wfile.write(bytes(de_auth_page, 'utf-8'))
        read_page(s, '/form.html')


def charge(s, body):
    cookie = s.headers.get('Cookie')
    simp_cookie = SimpleCookie(cookie)
    cookie_value = simp_cookie.get('auth')
    s.send_response(200)
    s.end_headers()
    if cookie_value.value == '1':
        params = parse_qs(body.decode())
        value = params['digit'][0]
        s.wfile.write(bytes("""<br><p><center><font face="impact" size="+3" color="#93B1B4">
        OK. Peter Parker had got %s$ when he had been in London.<br> I wonder if that was enought for him...
        </font></center></p>""" % value, 'utf-8'))
        read_page(s, '/charge.html')

    else:
        s.wfile.write(bytes('<br><p><center><font face="impact" size="+3" color="#93B1B4">'
                            'Error. No AUTH info.</font></center></p>', 'utf-8'))
        s.wfile.write(bytes('<p><br><br><center><a href="/form.html"><font face="verdana" size="+2" '
                            'color="#B2DDE1">BACK TO FORM</a></font></center></p>', 'utf-8'))


function_of_page = {
    '/': hello_page,
    '/hello_page.html': hello_page,
    '/form.html': form,
    '/auth.html': authorize,
    '/deauth.html': de_authorize,
    '/charge.html': charge
}
