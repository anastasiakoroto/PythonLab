from read_page_inf import read_page


def error_page(self, s_path):
    response, page = read_page(s_path)
    self.send_response(404)
    self.send_header('content-type', 'text/html')
    self.end_headers()
    self.wfile.write(page.encode('utf-8'))
