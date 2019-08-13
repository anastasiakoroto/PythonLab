import pytest
import json

import serializer

obj = serializer.Serializer()


class TestDeserializer:

    def test_check_format(self):
        string = '{"name":"Once Upon a Time in Hollywood", "director":"Tarantino"}'
        des_inp = obj.check_format(string)
        json_out = json.loads(string)
        assert des_inp == json_out

    def test_check_format_err(self):
        des_inp = obj.check_format('[]')
        out = 'Wrong data. It is not a json format.'
        assert des_inp == out

    @pytest.mark.parametrize('test_inp, out',
                             [("481516.2342", True),
                              ("4-8-15-16-23-42", False)], ids=['float-number', 'number with hyphen'])
    def test_is_number(self, test_inp, out):
        des_inp = obj.is_number(test_inp)
        assert des_inp == out

    def test_deserialize_digit(self):
        des_inp = obj.deserialize("4815162342")
        json_out = json.loads("4815162342")
        assert des_inp == json_out

    def test_deserialize_str(self):
        string = '"Kill Bill: Volume 2"'
        des_inp = obj.deserialize(string)
        json_out = json.loads(string)
        assert des_inp == json_out

    @pytest.mark.parametrize('test_inp, j_out', [('false', 'false'), ('true', 'true')])
    def test_deserialize_bool(self, test_inp, j_out):
        des_inp = obj.deserialize(test_inp)
        json_out = json.loads(j_out)
        assert des_inp == json_out

    @pytest.mark.parametrize('test_inp, out', [('[]', None), ('{}', None), ('null', None)])
    def test_deserialize_none(self, test_inp, out):
        des_inp = obj.deserialize(test_inp)
        assert des_inp == out

    def test_deserialize_array(self):
        string = '["Avengers", "Avengers: Age of Ultron", "Avengers: Infinity War", "Avengers: Endgame"]'
        des_inp = obj.deserialize(string)
        json_out = json.loads(string)
        assert des_inp == json_out

    def test_deserialize_dict(self):
        string = '{"Films about Hank Pym" :["Ant-Man", "Ant-Man and the Wasp", "Avengers: Endgame"]}'
        des_inp = obj.deserialize(string)
        json_out = json.loads(string)
        assert des_inp == json_out

    @pytest.mark.parametrize('t_inp, out', [
        ('{{"Films about Hank Pym" :["Ant-Man", "Ant-Man and the Wasp", "Avengers: Endgame"]}', {}),
        ('{"Films about Hank Pym" :]["Ant-Man", "Ant-Man and the Wasp", "Avengers: Endgame"]}', {}),
        ('{"Films about Hank Pym" :["Ant-Man"], "Ant-Man and the Wasp", "Avengers: Endgame"]}', {}),
        ('{"Films about Hank Pym" :["Ant-Man", "Ant-Man and the Wasp", "Avengers: Endgame"]', {}),
        ('{"Films about Hank Pym" :["Ant-Man", "Ant-Man and the Wasp", "Avengers: Endgame"}', {}),
        ('{"Films about Hank Pym" :"Ant-Man", "Ant-Man and the Wasp", "Avengers: Endgame"]}', {}),
        ('["Ant-Man", "Ant-Man and the Wasp", "Avengers: Endgame"', []),
        ('["Ant-Man", "Ant-Man and the Wasp", "Avengers: Endgame"]]', []),
        ('["Ant-Man", "Ant-Man and the Wasp",] "Avengers: Endgame"]', [])
    ], ids=['extra bracket { ', 'extra bracket ] A ', 'extra bracket ] B ', 'missing bracket } ', 'missing bracket ] ',
            'missing bracket [ ', 'missing bracket ] ', 'extra bracket ] C ', 'extra bracket ] D '])
    def test_deserialize_brackets(self, t_inp, out):
        des_inp = obj.deserialize(t_inp)
        assert des_inp == out

    @pytest.mark.parametrize('t_inp, out',
                             [
                                 ('{"Films about Hank Pym" :["Ant-Man", "Ant-Man and the Wasp",,"Avengers: Endgame"]}',
                                  {'Films about Hank Pym': []}),
                                 ('{"name":"Lord of Thunder",, "hobby":["Play with Mjoelnir and Axe", '
                                  '"Shoot lightning from his fingers"]}', {}),
                                 ('{"name":"Lord of Thunder", "hobby":["Play with Mjoelnir,,,, Axe", '
                                  '"Shoot lightning from his fingers"]}', {'name': 'Lord of Thunder', 'hobby':
                                     ['Play with Mjoelnir,,,, Axe', 'Shoot lightning from his fingers']}),
                                 ('{"name",:"Lord of Thunder"}', {})
                             ], ids=['extra comma between el. of list', 'extra comma between el. of dict',
                                     'extra comma in commas', 'extra comma before colon :'])
    def test_deserialize_comma(self, t_inp, out):
        des_inp = obj.deserialize(t_inp)
        assert des_inp == out

    def test_json_format(self):
        json_str = """
                {
                 "firstName":"Bruce",
                 "lastName":"Banner",
                 "isAlive":true,
                 "birthYear":1969,
                 "wife":null,
                 "characteristic":[
                   "Green",
                   "Dual personality"
                 ],
                 "friends":[
                   {
                     "name":"Thor", 
                     "career":"God of Thunder"
                   },
                   {
                     "name":"Black Widow", 
                     "career":"Spy"
                   }
                 ]
                }
        """
        des_inp = obj.check_format(json_str)
        json_out = json.loads(json_str)
        assert des_inp == json_out

    @pytest.mark.parametrize('t_inp, j_out',
                             [
                                 ('{"fullName": "Bruce \"Hulk\" Banner"}', {'fullName': 'Bruce "Hulk" Banner'}),
                                 ('{"database": "HowlingCommandos\\\\Survivor\\\\Bucky \"Winter Soldier\" Barnes"}',
                                  {'database': 'HowlingCommandos\\Survivor\\Bucky \"Winter Soldier\" Barnes'})
                             ])
    def test_deserialize_symbols(self, t_inp, j_out):
        des_inp = obj.deserialize(t_inp)
        json_out = json.loads(json.dumps(j_out))
        assert des_inp == json_out
