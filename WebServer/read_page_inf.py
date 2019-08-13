def read_page(s, s_path):
    try:
        page_to_open = open('pages' + s_path[21:], 'r').read()
    except OSError:
        s.send_response(404)
        page_to_open = open('pages/error.html', 'r').read()
    s.wfile.write(bytes(page_to_open, 'utf-8'))
