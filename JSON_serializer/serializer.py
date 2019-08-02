class Serializer:

    def serialize(self, obj):
        if type(obj) == str:
            if '"'or '\\' in obj:
                obj = self.replace_symbol(obj)
            return '"' + obj + '"'
        elif type(obj) in [int, float]:
            return str(obj)
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

    def replace_symbol(self, string):
        if '"' in string and '\\' in string:
            temp = string.replace('\\', '\\\\')
            temp_sec = temp.replace('"', '\\"')
            string = temp_sec
        elif '"' in string:  # commas in commas case
            temp = string.replace('"', '\\"')
            string = temp
        elif '\\' in string:  # '\' in string case
            temp = string.replace('\\', '\\\\')
            string = temp
        return string

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
                new_string = str(key) + ': ' + str(value)
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
            finish_note = attr_name + ': ' + str(attr_value)
            note.append(finish_note)
            finish_string = finish_string + finish_note + ', '
        finish_string = finish_string[:-2] + '}'
        return finish_string

    def if_array(self, initial_string):
        list_of_el = []  # list of separate strings
        new_list = []  # list with deserialized elements of initial array
        index = 0
        brackets_list = []  # stack with opened brackets
        begin_to_split = 0
        commas_opened = False
        check_exception = []
        for letter in initial_string:
            if letter == '"':
                commas_opened = not commas_opened
            elif letter in ['{', '[', ']', '}']:
                self.check_symbols(letter, brackets_list, check_exception)
                if len(check_exception) != 0:
                    return []
            elif letter == ',' and commas_opened is False and not brackets_list:
                if begin_to_split == index:
                    print('It cannot be deserialized. Probably you have extra comma.')  # extra comma case
                    return []
                else:
                    list_of_el.append(initial_string[begin_to_split: index])
                begin_to_split = index + 1
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
        check = []
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
            elif letter == ',' and commas_opened is False and colon is False and not brackets:  # extra comma case
                print('It cannot be deserialized. Probably you have extra comma.')
                return {}
            elif letter == '"':
                commas_opened = not commas_opened
            elif letter in ['{', '[', ']', '}']:
                self.check_symbols(letter, brackets, check)
                if len(check) != 0:
                    return []
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

    def check_symbols(self, current_letter, brackets_stack, check):
        if current_letter in ['[', '{']:
            brackets_stack.append(current_letter)
            return brackets_stack
        elif current_letter in ['}', ']']:
            try:
                if not brackets_stack:
                    raise ValueError
                if (current_letter == ']' and brackets_stack[-1] == '[') \
                        or (current_letter == '}' and brackets_stack[-1] == '{'):
                    brackets_stack.pop(-1)
                    return brackets_stack
                else:
                    raise ValueError
            except ValueError:
                check.append(1)
                print('Wrong data. It cannot be deserialized!')
                return check

    def is_number(self, n):
        try:
            float(n)
        except ValueError:
            return False
        return True

    def deserialize(self, string):
        if string == 'true' or string == 'false':
            return string == 'true'
        elif string[0] == '"':
            if '\\"' in string:  # commas in commas case
                temp_string = string.replace('\\"', '"')
                string = temp_string
            if '\\\\' in string:  # back slash case
                temp_string = string.replace('\\\\', '\\')
                string = temp_string
            return string[1:-1]
        elif string in ['[]', '{}', 'null']:
            return None
        elif string[0] in ['[', '{']:
            try:
                if string[0] == '[' and string[-1] == ']':
                    no_borders_str = string[1:-1]
                    return self.if_array(no_borders_str)
                elif string[0] == '{' and string[-1] == '}':
                    no_borders_str = string[1:-1]
                    if_dict = self.split_to_pairs(no_borders_str)
                    return self.make_dict(if_dict)
                else:
                    raise ValueError
            except ValueError:
                print('Wrong data. It cannot be deserialized |')
                if string[0] == '{':
                    return {}
                return []
        elif self.is_number(string):
            if float(string) % 1 == 0:
                number = float(string)
                return int(number)
            else:
                return float(string)

    def check_format(self, input_string):
        input_string = input_string.strip()
        if input_string[0] == '{':
            return self.deserialize(input_string)
        else:
            return 'Wrong data. It is not a json format.'
