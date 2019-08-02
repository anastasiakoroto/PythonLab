import pytest
import json

from JSON_serializer import serializer

obj = serializer.Serializer()


class TestSerializer:

    def test_serialize_str(self):
        init_data = 'Captain America'
        ser_inp = obj.serialize(init_data)
        json_out = json.dumps(init_data)
        assert ser_inp == json_out

    def test_serialize_digit(self):
        ser_inp = obj.serialize(48.15162342)
        out = '48.15162342'
        assert ser_inp == out

    @pytest.mark.parametrize("ser_inp,out",
                             [(True, True), (False, False)])
    def test_serialize_bool(self, ser_inp, out):
        inp = obj.serialize(ser_inp)
        json_out = json.dumps(out)
        assert inp == json_out

    def test_serialize_none(self):
        ser_inp = obj.serialize(None)
        json_out = json.dumps(None)
        assert ser_inp == json_out

    def test_serialize_array(self):
        init_data = ['Guardians of the Galaxy', 'Guardians of the Galaxy Vol.2']
        ser_inp = obj.serialize(init_data)
        json_out = json.dumps(init_data)
        assert ser_inp == json_out

    def test_serialize_dict(self):
        init_data = {'film_name': ['Guardians of the Galaxy', 'Guardians of the Galaxy Vol.2']}
        ser_inp = obj.serialize(init_data)
        json_out = json.dumps(init_data)
        assert ser_inp == json_out

    def test_serialize_obj(self):
        class StrangerThings:
            def __init__(self, serial_name, season_number, fallen):
                self.serial_name = serial_name
                self.season_number = season_number
                if fallen is None:
                    fallen = []
                self.fallen = fallen

        serial = StrangerThings('Stranger Things', 3, [{'name': 'Billy', 'diedLikeHero': True, 'totallyDied': True},
                                                       {'name': "Hopper", 'diedLikeHero': True, 'totallyDied': False}])
        inp_ser = obj.serialize(serial)
        out = '{"serial_name": "Stranger Things", "season_number": 3, ' \
              '"fallen": [{"name": "Billy", "diedLikeHero": true, "totallyDied": true},' \
              ' {"name": "Hopper", "diedLikeHero": true, "totallyDied": false}]}'
        assert inp_ser == out

    @pytest.mark.parametrize('test_input, test_output',
                             [({'fullName': "Bruce \"Hulk\" Banner"}, {'fullName': "Bruce \"Hulk\" Banner"}),
                              ({'database': 'S.H.I.E.L.D.\\The Avengers Initiative\\Spider-Man\\Peter Parker'},
                               {'database': 'S.H.I.E.L.D.\\The Avengers Initiative\\Spider-Man\\Peter Parker'})
                              ])
    def test_serialize_symbols(self, test_input, test_output):
        ser_inp = obj.serialize(test_input)
        json_out = json.dumps(test_output)
        assert ser_inp == json_out


if __name__ == '__main__':
    serializer_func = ['-v', 'Tests/serializer_test.py::TestSerializer']
    pytest.main(serializer_func)
