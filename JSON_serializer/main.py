import requests
import argparse
import sys
import os.path

import serializer
import const


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', dest='file_path', nargs='*', type=str,
                        help='decode file of defined directory '
                             '(which contains data in json format) from json to object')
    parser.add_argument('-u', dest='url', nargs='*', required=False, type=str,
                        help='decode data defined in URL from json to object ')
    parser.add_argument('-j', dest='json_string', nargs='*', required=False, type=str,
                        help='decode single quote string in json format from json to object')
    parser.add_argument('unknown_data', nargs='*', type=str, help='call instruction')
    return parser


def is_valid_file(arg):
    if not os.path.exists(arg):
        print(f'The file {arg} does not exist. Check your input data.')
        return False
    return True


def is_url(address):
    try:
        url = requests.get(address)
        return url.status_code == 200
    except requests.Timeout:
        raise requests.Timeout(f'There is a problem with access to url {address}. Hint: Timeout expired. Try again.')
    except requests.TooManyRedirects:
        raise requests.TooManyRedirects(f'There is a problem with access to url {address}. Hint: Too many redirects. ')
    except requests.ConnectionError:
        raise requests.ConnectionError(f'There is a problem with access to url {address}. Hint: Check your internet '
                                       f'connection (If there are no problems with internet, check correctness of '
                                       f'the input data). ')
    except requests.RequestException:
        raise requests.RequestException(f'There is a problem with access to url {address}. '
                                        f'Hint: Check correctness of the input data. ')


def file_argument(file_name):
    string_from_file = ''
    try:
        with open(file_name, 'r') as input_file:
            for line in input_file:
                temp = line.strip()
                string_from_file += temp
        if string_from_file != '':
            obj = serializer.Serializer().check_format(string_from_file)
            write_to_file(obj)
            return obj
        else:
            print('File has no data.')
            return string_from_file
    except PermissionError:
        raise PermissionError('File access issues.')
    except OSError:
        raise OSError(f'OSError. File with path/name {file_name} cannot be open.')


def write_to_file(decoded_string):
    if len(str(decoded_string)) < const.MAX_VALUE_OF_SYMBOLS:  # max value to write the data in terminal
        print(decoded_string)
    else:
        out_file = open('output.txt', 'w', encoding='utf-8')
        out_file.write(str(decoded_string))
        print('Deserialized object is too long. It was written to output.txt in this directory.')
        answer = input('Do you want to open this file in terminal? (y/n)')
        if answer in const.POSITIVE_ANSWERS:
            print('Deserialized object')
            print(decoded_string)
        out_file.close()


def url_argument(url_name):
    print('URL: ' + url_name)
    f = requests.get(url_name)
    my_file = f.text
    file_string = ''
    for symbol in my_file:
        file_string += symbol
    if file_string != '':
        file_string = file_string.strip()
        decoded_str = serializer.Serializer().check_format(file_string)
        write_to_file(decoded_str)
        return decoded_str
    else:
        print(f'The URL {url_name} has no data.')


def run_cmd_line():
    parser = create_parser()
    namespace = parser.parse_args(sys.argv[1:])
    term_string = ''
    if namespace.file_path:
        for i in namespace.file_path:
            term_string += i
        if is_valid_file(term_string):
            file_argument(term_string)
    elif namespace.url:
        for i in namespace.url:
            term_string += i
        if is_url(term_string):
            url_argument(term_string)
    elif namespace.json_string:
        for i in namespace.json_string:
            term_string += i
        string = term_string.strip()
        print('Your json-string: ' + string)
        st = serializer.Serializer().check_format(string)
        print(f'Deserialized: {st}')
    else:
        print('Instruction: You should point input data after script name. '
              'It can be path to file, url or string in json-format. '
              f'Use command\n $ python3 {sys.argv[0]} -h\nto see how you can run the program.')


if __name__ == '__main__':
    # serializer = serializer.Serializer()
    try:
        run_cmd_line()
    except Exception as e:
        print(e)
