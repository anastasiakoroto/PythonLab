import requests
import argparse
import sys
import os.path

import serializer


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('string', nargs='*', type=str)
    return parser


def is_url(address):
    try:
        url = requests.head(address)
        return url.status_code == 200
    except ValueError:
        return False


def file_argument(file_name):
    file = open(file_name, 'r', encoding='utf-8')
    string_from_file = ''
    for line in file:
        temp = line.strip()
        string_from_file += temp
    if string_from_file != '':
        obj = serializer.check_format(string_from_file)
        write_to_file(obj)
        file.close()


def write_to_file(decoded_string):
    if len(str(decoded_string)) < 500:
        print(decoded_string)
    else:
        out_file = open('output.txt', 'w', encoding='utf-8')
        out_file.write(str(decoded_string))
        print('Deserialized object is too long. It was written to output.txt in this directory.')
        answer = input('Do you want to open this file in terminal? (y/n)')
        if answer in ['y', 'yes', 'Y', 'YES']:
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
    file_string = file_string.strip()
    d = serializer.check_format(file_string)
    write_to_file(d)


def run_cmd_line():
    parser = create_parser()
    namespace = parser.parse_args(sys.argv[1:])
    term_string = ''
    if namespace.string:
        for i in namespace.string:
            term_string += i
        # check attribute: file, url or json_string
        if os.path.exists(term_string):
            file_argument(term_string)
        elif is_url(term_string):
            url_argument(term_string)
        else:
            string = term_string.strip()
            print(string)
            st = serializer.check_format(string)
            if type(st) == str:
                print('Unknown information. Check your input data.')


if __name__ == '__main__':
    serializer = serializer.Serializer()
    run_cmd_line()

