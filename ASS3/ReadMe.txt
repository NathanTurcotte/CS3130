Nathan Turcotte
5027975
CS3130
Assignement 3
	
Located in Directory ASS3 of repository CS3130
https://github.com/NathanTurcotte/CS3130

To execute client:
	python3 main.py client <ip> -p<port>
To execute server:
    python3 main.py server <ip> -p<port>

The -p option is optional(default 1060)


Consist of three Files
    main.py : Parses command line arguments, then calls the appropriate functions
    Client.py : Client Module
    Server.py : Server Module


Client Protocol :
    -Connects to the server
    -commands are sent as is, encoded in ascii format
         If the user writes "SignIn Bob", "SignIn Bob" is sent to the server
    -Data received from the server, is decoded from ascii format and Displayed as is in the console using the print command
    -Typing "exit" will exit the program
        Doing so will Send the server a signout message
    -The client does not hold any information on it's username or status
        The server is entirely responsible of this information, based on it's data, and the address messages are received from

Server Protocol :
    -The server receives the message.
    -The messages command is then determined.
       -ie : first alphabetical word, seperated by whitespace, starting from the beggining of the text
            If the command is supported, the approriate data is passed to a function
            that will return text to be sent back to the sender
    -Accepted usernames are stored in a list named Existing
    -A list of online users is stored in OnLine, entries added to this list are of form (<username>, <address>)

Client Commands :

    Commands are Case-Sensitive

    Help
        Request Help Message
    SignIn <username>
        The following usernames are allowed : Bob, John, Nathan, Franco
        More may be added by adding entries in the Existing List found in Server.py
        Messages sent to you while offline will be displayed
    SignOut
        Will attempt to log out anyone at the address who send the request
    WhoIsOn
        Returns a list of online users
    Send <username> <Message>
        Send a user a message, if the user is offline, the message is stored.
    Exit
        Exits client, also sends a SignOut request

Warning:
    Exiting from a client without previously calling SignOut or using Exit 
        Will cause the username to be unusable until the server is restarted
        As the server will not be notified of the action
    
    

        

