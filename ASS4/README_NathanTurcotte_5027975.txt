Nathan Turcotte
5027975
CS3130
Assignement 4
TCP Employee Management System
	
Located in Directory ASS4 of repository CS3130
https://github.com/NathanTurcotte/CS3130

To execute client:
	python3 main.py client <ip> -p<port>
To execute server:
    python3 main.py server <ip> -p<port>

The -p option is optional(default 1060)


Consist of seven Files
    main.py : Parses command line arguments, then calls the appropriate functions
    Client.py : Client Module
    Server.py : Server Module
    cdb.py : Client Database Interaction Module (Promts and formats input)
    database.py : Server Database interaction Module, (file manipulation, adding removing...)
    ra.py : receiveAll function
    data.txt : database(employee records)


Client Protocol :
    -Connects to server, sends request, waits for reply, closes connection
    -Messages are sent, encoded in 'ascii'.
        -End of message is marked by the ';' character
        -seperate fields within the message are delimited by the ':' token
          -The first token is always an identifier for which action to execute
            -AddEmployee request : "add:id:fname:lname:depart:;"
            -FindEmployee request : "find:id:;"
            -RemoveEmployee request : "remove:id:;"
            -DisplayEmployee request : "display:;"
    -Messages received are to be decoded, then printed as is.
    -Employee Id can contain any number of digits 0-9
    -First name, last name, department can contain any number of characters a-zA-Z

Server Protocol :
    -The server listens for connections
    -When a connection is requested, a new socket is created
    -The server waits for a message, executes the message, then replys.
        -Client messages are split into a list delimited by ":"
            ex : AddEmployee 
                message = "add:52:nathan:Turcotte:science:" -> ["add","52","nathan","Turcotte","Science",""]
            the list is then sent to the appropriate function to execute. The function in turn returns text to be sent back to the client
    -The server appends the ";" character to messages to be sent back to the client, and closes the connection

    
Client/Server
    -All data is sent encoded in 'ascii'
    -Messages must end with the ';' character
        -The receiveMessage function is responsible of decoding, while the client Send, server Send, are responsible for encoding
    

        

