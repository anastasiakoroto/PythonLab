import sys
import argparse
import os.path
import requests


class StrangerThings:

    def __init__(self, serial_name, season_number, amount_of_ser, ser_names, fallen):
        self.serial_name = serial_name
        self.season_number = season_number
        self.amount_of_series = amount_of_ser
        if ser_names is None:
            ser_names = []
        self.ser_names = ser_names
        if fallen is None:
            fallen = []
        self.fallen = fallen


serial = StrangerThings('Stranger Things', 3, 8,
                        ["Suzie, Do You Copy?", "The Mall Rats", "Case of the Missing Lifeguard", 'The Sauna Test',
                         'The Flayed', 'E Pluribus Unum', 'The Bite', 'The battle of Starcourt'],
                        [{'name': 'Billy', 'diedLikeHero': True, 'totallyDied': True},
                         {'name': "Hopper", 'diedLikeHero': True, 'totallyDied': False}])


class Serializer:

    def serialize(self, obj):
        if type(obj) == str:
            return '"' + obj + '"'
        elif type(obj) in [int, float]:
            return obj
        elif type(obj) is bool:
            return str(obj).lower()
        elif obj is None:
            return 'null'
        elif type(obj) in [list, tuple]:
            return self.if_list(obj)
        elif type(obj) == dict:
            return self.if_dict(obj)
        else:
            return self.if_other(obj)

    def if_list(self, obj):
        if len(obj) != 0:
            attr_value_list = '['
            for attr in obj:
                new_attr = self.serialize(attr)
                attr_value_list = attr_value_list + new_attr + ', '
            attr_value_list = attr_value_list[:-2]
            return attr_value_list + ']'
        else:
            return '[]'

    def if_dict(self, obj):
        if len(obj) != 0:
            attr_value_dict = '{'
            for attr in obj:
                key = self.serialize(attr)
                value = self.serialize(obj[attr])
                new_string = str(key) + ':' + str(value)
                attr_value_dict = attr_value_dict + new_string + ', '
            attr_value_dict = attr_value_dict[:-2]
            attr_value_dict += '}'
            return attr_value_dict
        else:
            return '{}'

    def if_other(self, obj):
        note = []
        finish_string = '{'
        for attribute in obj.__dict__:
            attr_name = self.serialize(attribute)
            attr_value = self.serialize(getattr(obj, attribute))
            finish_note = attr_name + ':' + str(attr_value)
            note.append(finish_note)
            finish_string = finish_string + finish_note + ', '
        finish_string = finish_string[:-2] + '}'
        return finish_string


class Deserializer:

    def if_array(self, string_arr):
        initial_string = string_arr[1:-1]
        list_of_el = []  # list of separate strings
        new_list = []  # list with deserialized elements of initial array
        index = 0
        brackets_list = []  # stack with opened brackets
        begin_to_split = 0
        commas_opened = False
        for letter in initial_string:
            if letter == '"':
                commas_opened = not commas_opened
            elif letter == ',' and commas_opened is False:
                try:
                    if not brackets_list:
                        list_of_el.append(initial_string[begin_to_split: index])
                        begin_to_split = index + 1
                except ValueError:
                    print('Wrong. This data cannot be deserialized')
                    return []
            elif letter == '{' or letter == '[':
                brackets_list.append(letter)
            elif letter in ['}', ']']:
                try:
                    if not brackets_list:
                        raise ValueError
                    if (letter == ']' and brackets_list[-1] == '[') or (letter == '}' and brackets_list[-1] == '{'):
                        brackets_list.pop(-1)
                    else:
                        raise ValueError
                except ValueError:
                    print('Wrong data. It cannot be deserialized...')
                    return []  # check what json returns actually
            if index == len(initial_string) - 1:
                list_of_el.append(initial_string[begin_to_split: index + 1])
            index += 1
        for i in range(len(list_of_el)):
            temp = list_of_el[i].strip()
            des_element = self.deserialize(temp)  # deserialized element of list of all strings
            new_list.append(des_element)
        return new_list

    def split_to_pairs(self, string):
        pairs = []
        key_ch = False  # check if key found
        value_ch = False  # check if value found
        index = 0
        begin_of_split = 0
        commas_opened = False
        colon = False  # check if separator found
        brackets = []  # stack with open brackets
        for letter in string:
            if letter == ':' and commas_opened is False and not brackets:
                colon = not colon
                key = string[begin_of_split: index]
                key_ch = not key_ch
                begin_of_split = index + 1
            elif letter == ',' and commas_opened is False and colon is True and not brackets:
                value = string[begin_of_split: index]
                value_ch = not value_ch
                begin_of_split = index + 1
            elif letter == '"':
                commas_opened = not commas_opened
            elif letter in ['[', '{']:
                brackets.append(letter)
            elif letter in ['}', ']']:
                try:
                    if not brackets:
                        raise ValueError
                    if (letter == ']' and brackets[-1] == '[') or (letter == '}' and brackets[-1] == '{'):
                        brackets.pop(-1)
                    else:
                        raise ValueError
                except ValueError:
                    print('Wrong data. It cannot be deserialized!')
                    return []  # check what json returns actually
            try:
                if not brackets and index == (len(string) - 1):
                    value = string[begin_of_split: index + 1]
                    value_ch = not value_ch
                elif index == (len(string) - 1) and brackets:
                    raise ValueError
            except ValueError:
                print('Wrong data. ' + str(len(brackets)) + ' of brackets without pair. It cannot be deserialized.')
                return {}
            if key_ch is True and value_ch is True:
                pairs.append((key, value))
                key_ch, value_ch, colon = False, False, False
            index += 1
        return pairs

    def make_dict(self, pairs_list):
        object_dict = {}
        for i in pairs_list:
            temp_1 = i[0].strip()
            temp_2 = i[1].strip()
            key = self.deserialize(temp_1)
            value = self.deserialize(temp_2)
            object_dict[key] = value
        return object_dict

    def is_number(self, n):
        try:
            float(n)
        except ValueError:
            return False
        return True

    def deserialize(self, string):
        if string == 'true' or string == 'false':
            return string == 'true'
        elif string in ['[]', '{}', 'null']:
            return None
        elif string[0] == '"':
            return string[1:-1]
        elif string[0] == '[':
            try:
                if string[-1] == ']':
                    return self.if_array(string)
                else:
                    raise ValueError
            except ValueError:
                print('Wrong data. It cannot be deserialized.')
                return []
        elif string[0] == '{':
            try:
                if string[-1] == '}':
                    no_borders_str = string[1:-1]
                    if_dict = self.split_to_pairs(no_borders_str)
                    return self.make_dict(if_dict)
                else:
                    raise ValueError
            except ValueError:
                print('Wrong data. It cannot be deserialized :(')
                return {}
        elif self.is_number(string):
            if float(string) % 1 == 0:
                number = float(string)
                return int(number)
            else:
                return float(string)


ser = Serializer()
ss = ser.serialize(serial)
print('Serialized string: ')
print(ss, end='\n\n')

des = Deserializer()
print('Deserialized object: ')
print(des.deserialize(ss), end='\n\n')


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


if __name__ == '__main__':
    parser = create_parser()
    namespace = parser.parse_args(sys.argv[1:])
    term_string = ''
    if namespace.string:
        for i in namespace.string:
            term_string += i
        # check attribute: file, url or json_string
        if os.path.isfile('./' + term_string):
            file = open(term_string, 'r', encoding='utf-8')
            string_from_file = ''
            for line in file:
                temp = line.strip()
                string_from_file += temp
            if string_from_file != '':
                d = des.deserialize(string_from_file)
                if len(str(d)) < 500:
                    print(d)
                else:
                    out_file = open('output.txt', 'w', encoding='utf-8')
                    out_file.write(str(d))
                    print('Deserialized object is too long. It was written to output.txt in this directory.')
                    answer = input('Do you want to open this file in terminal? (y/n)')
                    if answer in ['y', 'yes', 'Y', 'YES']:
                        print('Deserialized object')
                        print(d)
                    out_file.close()
                file.close()
        elif is_url(term_string):
            print('URL: ' + term_string)
            f = requests.get(term_string)
            my_file = f.text
            file_string = ''
            for i in my_file:
                file_string += i
            file_string = file_string.strip()
            d = des.deserialize(file_string)
            if len(str(d)) < 500:
                print('Deserialized object: ')
                print(d)
            else:
                out_file = open('output.txt', 'w', encoding='utf-8')
                out_file.write(str(d))
                print('Deserialized object is too long. It was written to output.txt in this directory.')
        else:
            print('Deserialized object: ')
            print(des.deserialize(term_string))
