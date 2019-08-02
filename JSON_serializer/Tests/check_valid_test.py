import pytest
from unittest import mock
from requests import RequestException, ConnectionError, Timeout, TooManyRedirects

from JSON_serializer import main


class TestValid:

    def test_is_valid_file(self):
        inp = main.is_valid_file('/home/anastasiya/Downloads/ironman.txt')
        out = True
        assert inp == out

    def test_is_valid_file_err(self):
        inp = main.is_valid_file('ironman.txt')
        out = False
        assert inp == out

    def test_open_file(self):
        with mock.patch('JSON_serializer.main.open') as opened:
            opened.side_effect = OSError
            with pytest.raises(OSError):
                main.file_argument('blackpanther.txt')

    def test_open_file_permission(self):
        with mock.patch('JSON_serializer.main.open') as opened:
            opened.side_effect = PermissionError
            with pytest.raises(PermissionError):
                main.file_argument('/home/nickfury/work/The Avengers Initiative/characteristics/falcon.txt')

    def test_valid_path(self):
        with mock.patch('os.path.exists') as path:
            path.return_value = False
            assert main.is_valid_file('/home/nickfury/work/The Avengers Initiative/characteristics/hulk.txt') == False

    def test_is_url_err(self):
        inp = main.is_url('https://www.harrypotter.com')
        out = False
        assert inp == out

    @mock.patch.object(main.requests, "get", side_effect=Timeout)
    def test_is_url_timeout(self, mock_requests_get='https://peggycarter.org'):
        with pytest.raises(Timeout):
            main.requests.get(mock_requests_get)

    @mock.patch.object(main.requests, "get", side_effect=ConnectionError)
    def test_is_url_connection_error(self, mock_requests_get='https://www.marvel.com/'):
        with pytest.raises(ConnectionError):
            main.requests.get(mock_requests_get)

    @mock.patch.object(main.requests, "get", side_effect=TooManyRedirects)
    def test_is_url_redirects_except(self, mock_requests_get=
                                   'https://www.amazon.in/Thor-Hammer-Logo-Keychain-Metal'
                                   '/dp/B01F1QGBHI/ref=sr_1_3?keywords=thor&qid=1564739314&s=electronics&sr=1-3'):
        with pytest.raises(TooManyRedirects):
            main.requests.get(mock_requests_get)

    @mock.patch.object(main.requests, "get", side_effect=RequestException)
    def test_is_url_request_except(self, mock_requests_get='http://www.captainameriac.com/'):
        with pytest.raises(RequestException):
            main.requests.get(mock_requests_get)


if __name__ == '__main__':
    valid_func = ['-v', 'check_valid_test.py::TestValid']
    pytest.main(valid_func)
