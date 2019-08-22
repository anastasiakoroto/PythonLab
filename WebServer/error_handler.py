from read_page_inf import read_page
from const import SERVERS_HOST, SERVER_TWO_PORT


def not_found_page(self):
    back_to_form = False
    error_dict = {'title': 'ERROR', 'error_status': 404, 'message': 'Page not found', 'back_to_form': back_to_form,
                  'server_two_host': SERVERS_HOST, 'server_two_port': SERVER_TWO_PORT}
    page = read_page('/error.html', **error_dict)
    self.send_response(404)
    self.send_header('content-type', 'text/html')
    self.end_headers()
    self.wfile.write(page)