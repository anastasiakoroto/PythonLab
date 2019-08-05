import pytest
from unittest import mock
from requests import ConnectionError, Timeout, RequestException, TooManyRedirects

import main


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
        with mock.patch('main.open') as opened:
            opened.side_effect = OSError
            with pytest.raises(OSError):
                file_name = 'blackpanther.txt'
                main.file_argument(file_name)

    def test_open_file_permission(self):
        with mock.patch('main.open') as opened:
            opened.side_effect = PermissionError
            with pytest.raises(PermissionError):
                file_path = '/home/nickfury/work/The Avengers Initiative/characteristics/falcon.txt'
                main.file_argument(file_path)

    def test_valid_path(self):
        with mock.patch('os.path.exists') as path:
            path.return_value = False
            assert main.is_valid_file('/home/nickfury/work/The Avengers Initiative/characteristics/hulk.txt') == False

    @mock.patch.object(main.requests, "get")
    def test_is_url_timeout(self, mock_requests_get):
        mock_requests_get.side_effect = Timeout
        with pytest.raises(Timeout):
            main.is_url('https://peggycarter.org')

    @mock.patch.object(main.requests, "get")
    def test_is_url_connection_error(self, mock_requests_get):
        mock_requests_get.side_effect = ConnectionError
        with pytest.raises(ConnectionError):
            main.is_url('https://www.marvel.com/')

    @mock.patch.object(main.requests, "get")
    def test_is_url_redirects_except(self, mock_requests_get):
        mock_requests_get.side_effect = TooManyRedirects
        with pytest.raises(TooManyRedirects):
            main.is_url('https://www.amazon.in/Thor-Hammer-Logo-Keychain-Metal'
                                   '/dp/B01F1QGBHI/ref=sr_1_3?keywords=thor&qid=1564739314&s=electronics&sr=1-3')

    @mock.patch.object(main.requests, "get")
    def test_is_url_request_except(self, mock_requests_get):
        mock_requests_get.side_effect = RequestException
        with pytest.raises(RequestException):
            main.is_url('http://www.captainameriac.com/')

    def test_json_from_url(self):
        with mock.patch('main.requests') as mock_requests:
            mock_requests.get.return_value.text = """  {
                                                         "fruit": "Apple",
                                                         "size": "Large",
                                                         "color": "Red"
                                                       }
            """
            url_address = 'https://support.oneskyapp.com/hc/en-us/article_attachments/202761627/example_1.json'
            assert main.url_argument(url_address) == {"fruit": "Apple", "size": "Large", "color": "Red"}

    def test_json_from_url_err(self):
        with mock.patch('main.requests.get') as mock_requests:
            mock_requests.return_value.text = 'not json data'
            url_address = 'https://www.marvel.com'
            main.url_argument(url_address)
            mock_requests.assert_called_with(url_address)

    def test_json_from_file_err(self):
        with mock.patch('main.open') as mock_file:
            mock_file.read.return_value = ''
            file_name = '~/PycharmProjects/JSON_serializer/altron.txt'
            response = main.file_argument(file_name)
            assert response == ''

    def test_url_invalid_json(self):
        with mock.patch('main.requests.get') as mocked_get:
            mocked_get.return_value.status_code = 400
            valid_url = main.is_url('https://www.marvel.com')
            if valid_url:
                res = main.url_argument('https://www.marvel.com')
                assert res == 'Wrong data. It is not a json format.'


if __name__ == '__main__':
    valid_func = ['-v', 'check_valid_test.py::TestValid']
    pytest.main(valid_func)
