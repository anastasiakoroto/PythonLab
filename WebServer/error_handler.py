from read_page_inf import read_page


def not_found_page(self, s_path):
    _, page = read_page(s_path, error_status=404, message='<br />Page not found', back_to_form='')
    self.send_response(404)
    self.send_header('content-type', 'text/html')
    self.end_headers()
    self.wfile.write(page.encode('utf-8'))
