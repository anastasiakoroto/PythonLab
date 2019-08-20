def read_page(s_path, **context):
    try:
        page_to_open = open('pages' + s_path, 'r').read()
        response_status = 200
    except OSError:
        page_to_open = open('pages/error.html', 'r').read()
        response_status = 404
    if len(context) > 0:
        page_to_open = page_to_open.format(**context)
        return response_status, page_to_open
    else:
        return response_status, page_to_open
