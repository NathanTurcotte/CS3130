MAX_BYTES = 65535

import socket
import threading
from threading import Thread
import re

Commands = ["SignIn", "WhoIsOn", "Send", "SignOut", "Help", "WhoIsOn"]
OnLine = []
Existing = ["Bob", "John", "Nathan", "Franco"]
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#Restrict access to the OnLine set
onlineLock = threading.Lock()
printLock = threading.Lock()
#Restrict access to sock
sendLock = threading.Lock()
#Restrict file io to one thread at a time
fileLock = threading.Lock()

class ExecuteQuery(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self, data, address):
        """
            Performs the query
            Data contains the entire text send by the user
            Step 1 : determime which command was entered
            Step 2 : call the appropriate function
                     functions that require the text, are sent the complete message
            Step 3 : The called functions will return the text that is to be sent back to the sender
        """
        text = data.decode('ascii')
        reply = ""
        match = re.match("[a-zA-Z]+", text, 0)
        if match:
            if match.group() not in Commands:
                reply = "Unknown Command : " + match.group()
            else:
                if (match.group() == "SignIn"):
                    reply = ClientSignIn(text, address)
                    Print("Sign In request from : " + str(address))
                elif (match.group() == "Help"):
                    reply = ClientHelp()
                    Print("Help request from : " + str(address))
                elif (match.group() == "Send"):
                    reply = ClientSend(text, address)
                    Print("Send request from : " + str(address))
                elif (match.group() == "SignOut"):
                    reply = ClientSignOut(address)
                    Print("Sign out request from : " + str(address))
                elif (match.group() == "WhoIsOn"):
                    reply = WhoIsOn()
                    Print("WhoIsOn request from : " + str(address))
                else:
                    reply = "Command Not Handled"

        else:
            reply = "Unknown Command"
        Send(reply, address)
                             
            

def run (ip, port):
    """
        Continuously receive from socket
        When a message is received, start a thread, passing the entire message and address
        then continue listening
    """
    sock.bind((ip,port))
    print("Server Listening at: ", sock.getsockname())
    while True:
        data, address = sock.recvfrom(MAX_BYTES)
        ExecuteQuery().run(data,address)  

def Print(text):
    """
        Print text to server console
        Uses printLock to prevent two threads from outputting text at the same time
    """
    printLock.acquire()
    print(text)
    printLock.release()
def Send(data, address):
    """
        Send data(string format) to the given address
        Uses sendLock to prevent multiple threads attempting to use sock simultaneously
    """
    reply = "(Server) " + data
    sendLock.acquire()
    sock.sendto(reply.encode('ascii'), address)
    sendLock.release()

def WhoIsOn():
    """
        Returns a string containing the username of online users
    """
    onlineLock.acquire()
    reply = str(len(OnLine)) + " user(s) currently online\n"
    for i in range(0,len(OnLine)):
        reply += "  " + OnLine[i][0] +'\n'
    onlineLock.release()
    return reply
        

def ClientSignIn(text, address):
    """
        Attempts a client SignIn
        text = entire message sent from client
        address = clients address
    """
    tokens = text.split(' ')
    if len(tokens) == 2:
        if tokens[1] not in Existing:
            return "User: " + tokens[1] + ". Does Not Exist."
        onlineTag = isOnline(tokens[1], address)
        if onlineTag == 1:
            return "User: " + tokens[1] + ". Is allready Signed in"
        if onlineTag == 2:
            return "Multiple Signins from one client detected"
        setOnline(tokens[1], address)
        return FetchFile(tokens[1])
        
    else:
        return "Improper SignIn information. Expected format : SignIn <username>"

def ClientHelp():
    """
        Return help message
    """
    text  = "Welcome to MMS!\n"
    text += "--"
    text += "The following Commands are supported\n"
    text += "   SignIn <username>\n"
    text += "   WhoIsOn\n"
    text += "   Send <username> <Message>\n"
    text += "   SignOut\n"
    text += " Commands are Case-Sensitive"
    return text

def ClientSend(text,senderAddress):
    """
        Send message from Sender Address to the user designated in text(complete command)
        Check if the sender is online. Ie is address is located in the OnLine set
        Check if the receiver is exist and is online. 
    """
    tokens = text.split(' ')
    #tokens[0] will contain the command, while tokens[1] will contain the receivers name
    message = ""
    if len(tokens) < 2:
        return "Improper use of Send Command. Expected format : Send <username> <message>"
    elif tokens[1] in Existing:
        senderName = GetClientName(senderAddress)
        if senderName == "":
            return "You must be signed in to send messages"
        message = senderName + " : "
        #put the message back together, tokens[2] and beyond contain the actual text
        for i in range(2, len(tokens)):
            message += tokens[i] + " "
        if isOnline(tokens[1], 0):
            Found, receiverAddress = GetClientAddress(tokens[1])
            if Found:
                Send(message, receiverAddress)
        else:         
            message = tokens[1] + " is currently offline. " + StoreClientMessage(tokens[1],message)
    else:
        message = tokens[1] + " Does not exist!"
    return message
 

def ClientSignOut(addr):
    """
        Signs out (remove entry from OnLine set) client at given address
        Checks if a user is connected at the given address first
    """
    found = -1
    reply = ""
    onlineLock.acquire()
    for i in range(0,len(OnLine)):
        if OnLine[i][1] == addr:
            found = i
            break
    if (found != -1):
        del OnLine[found]
        reply = "Sign Out successful!"  
    else:
        reply = "You can not Sign Out if you have not Signed In"
    onlineLock.release()
    return reply

def StoreClientMessage(user, message):
    """
        Stores a message to an offline user
        text in message must be of format
        <sender> : <message>
        new line character added by this function
    """
    fileLock.acquire()
    reply = "Message successfully saved!"
    try:
        f = open("Clients/"+user, "a")
        f.write(message)
        f.write('\n')
        f.close()
    except IOError:
        reply = "Error saving Message"
    fileLock.release()
    return reply

def FetchFile(username):
    """
        Looks for existing messages sent to the user while offline
        Message data is stored into the file exactly as it is suppose to be output
    """
    messages = []
    fileLock.acquire()
    try:
        f = open("Clients/"+username, 'r')
        lines = f.readlines()
        for i in range(0,len(lines)):
            match = re.match("[a-zA-z0-9] :", lines[i], 0)
            if not match:
                messages.append(lines[i])
        f.close()
    except IOError :
        messages = []
    finally:    
        s = open("Clients/"+username, 'w')
        s.close()
        fileLock.release()
    reply = "Welcome Back " + username + "! You have " + str(len(messages)) + " new message(s).\n"
    for i in range(0,len(messages)):
        reply += messages[i] 
    return reply

def isOnline(name, address):
    """
        Returns 1 if the user with name is online
        Returns 2 of the user with address(ip,port) is online
        0 otherwise
    """
    onlineLock.acquire()
    Found = 0
    for i in range(0,len(OnLine)):
        if name == OnLine[i][0]:
            Found = 1
        if address == OnLine[i][1]:
            Found = 2
    onlineLock.release()
    return Found

def GetClientName(addr):
    """
        Returns the clients name at the given address
        Returns "" if a match can not be made
    """
    name = ""
    onlineLock.acquire()
    for i in range(0,len(OnLine)):
        if addr == OnLine[i][1]:
            name = OnLine[i][0]
            break   
    onlineLock.release()
    return name

def GetClientAddress(username):
    """
        Get the address of a givne username
        Returns Found, address
        a valid address is only given if Found is set to true
    """
    onlineLock.acquire()
    Found = False
    addr = ""
    for i in range(0,len(OnLine)):
        if username == OnLine[i][0]:
            addr = OnLine[i][1]
            Found = True
            break
    onlineLock.release()
    return Found, addr
def setOnline(username, address):
    """
        Add a user with (username,address) to the OnLine set
    """
    onlineLock.acquire()
    OnLine.append([username, address])
    onlineLock.release()
