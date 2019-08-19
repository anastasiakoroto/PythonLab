def read_page(s_path, **html_messages):
    try:
        page_to_open = open('pages' + s_path[21:], 'r').read()
        response_status = 200
    except OSError:
        page_to_open = open('pages/error.html', 'r').read()
        response_status = 404
    if len(html_messages) > 0:
        page_to_open = page_to_open.format(**html_messages)
        return response_status, page_to_open
    else:
        return response_status, page_to_open