from http.cookies import SimpleCookie
from urllib.parse import parse_qs


def read_page(s_path, **html_messages):
    try:
        page_to_open = open('pages' + s_path, 'r').read()
        response_status = 200
    except OSError:
        page_to_open = open('pages/error.html', 'r').read()
        response_status = 404
    if len(html_messages) > 0:
        page_to_open = page_to_open.format(**html_messages)
        return response_status, page_to_open
    else:
        return response_status, page_to_open


def hello_page(s):
    response, page = read_page('/hello_page.html')
    s.send_response(response)
    s.send_header('content-type', 'text/html')
    s.end_headers()
    s.wfile.write(page.encode('utf-8'))


def authorize(s):
    response, page = read_page('/auth.html')
    s.send_response(response)
    s.send_header('content-type', 'text/html')
    s.send_header('Set-Cookie', 'auth=1; HttpOnly')
    s.end_headers()
    s.wfile.write(page.encode('utf-8'))


def de_authorize(s):
    response, page = read_page('/deauth.html')
    s.send_response(response)
    s.send_header('content-type', 'text/html')
    s.send_header('Set-Cookie', 'auth=0; HttpOnly')
    s.end_headers()
    s.wfile.write(page.encode('utf-8'))


def form(s):
    cookie = s.headers.get('Cookie')
    simple_cookie = SimpleCookie(cookie)
    cookie_value = simple_cookie.get('auth')
    title = '<p><font color="#B2DDE1" face="impact" size="+3">form page</font></p>'
    if cookie_value.value == '0' or cookie_value is None:
        auth_page = '<p><a href="/auth.html"><font color="#899597" size="+1" face="verdana">AUTHORIZE' \
                    '</font></a></p>'
        response, page = read_page('/form.html', page_title=title, auth_page=auth_page)
    else:
        de_auth_page = '<p><a href="/deauth.html"><font color="#899597" size="+1" face="verdana">DE-AUTHORIZE' \
                       '</font></a></p>'
        response, page = read_page('/form.html', page_title=title, auth_page=de_auth_page)
    s.send_response(response)
    s.send_header('content-type', 'text/html')
    s.end_headers()
    s.wfile.write(page.encode('utf-8'))


def charge(s, body):
    cookie = s.headers.get('Cookie')
    simp_cookie = SimpleCookie(cookie)
    cookie_value = simp_cookie.get('auth')
    if cookie_value.value == '1':
        params = parse_qs(body.decode())
        value = params['digit'][0]
        message = f"""<br/><p><center><font face="impact" size="+3" color="#93B1B4"> OK. Peter Parker had got 
        {value}$ when he had been in London.<br /> I wonder if that was enough for him...</font></center></p>"""
        response, page = read_page('/charge.html', message=message)
    else:
        auth_message = """<br /><p><center><font face="impact" size="+3" color="#93B1B4">
            Error. No AUTH info.</font></center></p>"""
        response, page = read_page('/charge.html', message=auth_message)
    s.send_response(response)
    s.send_header('content-type', 'text/html')
    s.end_headers()
    s.wfile.write(page.encode('utf-8'))


def error_page(s):
    response, page = read_page('/error.html')
    s.send_response(404)
    s.send_header('content-type', 'text/html')
    s.end_headers()
    s.wfile.write(page.encode('utf-8'))


function_of_page = {
    '/': hello_page,
    '/hello_page.html': hello_page,
    '/form.html': form,
    '/auth.html': authorize,
    '/deauth.html': de_authorize,
    '/error.html': error_page
}
