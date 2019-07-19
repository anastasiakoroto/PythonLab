# JSON serializer
About project
-------------------
The program:
* serializes object into JSON, 
* deserializes string in JSON format into object.

***Exapmles:***  
_-Deserialized object:_
```
{'serial_name': 'Stranger Things', 'season_number': 3, 'amount_of_series': 8, 'ser_names': ['Suzie, Do You Copy?', 'The Mall Rats', 'Case of the Missing Lifeguard', 'The Sauna Test', 'The Flayed', 'E Pluribus Unum', 'The Bite', 'The battle of Starcourt'], 'fallen': [{'name': 'Billy', 'diedLikeHero': True, 'totallyDied': True}, {'name': 'Hopper', 'diedLikeHero': True, 'totallyDied': False}]}
```
_- Serialized string:_
```
{"serial_name":"Stranger Things", "season_number":3, "amount_of_series":8, "ser_names":["Suzie, Do You Copy?", "The Mall Rats", "Case of the Missing Lifeguard", "The Sauna Test", "The Flayed", "E Pluribus Unum", "The Bite", "The battle of Starcourt"], "fallen":[{"name":"Billy", "diedLikeHero":true, "totallyDied":true}, {"name":"Hopper", "diedLikeHero":true, "totallyDied":false}]}
```


How to run
------------------
To run the program from terminal it needs to point interpreter and name of the file (**main.py**) and after that point additional argument: path to file, link or string (must be written in single quots), which contains the information in json format. The last argument is optional.  

***Examples:***  
```
$ python3 main.py /path/to/file/file_name.txt
$ python3 main.py http://api.plos.org/search?q=title:DNA
$ python3 main.py '{"name":"Eminem", "hobby":"rap", "age":46, "albums":["Kamikaze", "Revival"]}'  
```
