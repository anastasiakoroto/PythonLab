# Task 1 
## About project
The program:  
* processes the HTTP-request
* works with cookie (can authorize or de-authorize the user)
* interacts with HTML-pages.

__One server used.__  
  
    
Pages functions:
* _auth.html_ - print message about successful authorization, link back to _form.html_ page is located here
* _deauth.html_ - print message about successful de-authorization, link back to _form.html_ page is located here
* _form.html_ - send the entered data to _charge.html_, on this page authorization and de-authorization buttons are located
* _charge.html_ - if user is logged in, print succesful message, otherwise a message about the lack of authorization. Link back to _form.html_ page is located here
* _error.html_ - print error message

## How to run
To run the program from terminal you need to:
* Open the folder of this project.  
_Example:_
`$ cd user/path/to/project`
* Point interpreter and name of the file (__server.py__) and then write port number - __8001__.  
_Example:_
`$ python3 server.py 8001`
* Enter any of these addresses:  
http://localhost:8001/  
http://localhost:8001/hello_page.html  
http://localhost:8001/form.html  
