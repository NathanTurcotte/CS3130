MAX_BYTES = 65535

import socket
import threading
from threading import Thread
import re

Commands = ["SignIn", "WhoIsOn", "Send", "SignOut", "Help"]
OnLine = []
Existing = ["Bob", "John"]
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

class ExecuteQuery(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self, data, address):
        text = data.decode('ascii')
        reply = ""
        match = re.match("[a-zA-Z]+", text, 0)
        if match:
            if match.group() not in Commands:
                reply = "Unknown Command : " + match.group()
            else:
                if (match.group() == "SignIn"):
                    reply = ClientSignIn(text, address)
                elif (match.group() == "Help"):
                    reply = ClientHelp()
                elif (match.group() == "Send"):
                    reply = ClientSend(text, address)
                elif (match.group() == "SignOut"):
                    reply = ClientSignOut(address)
                else:
                    reply = "Command Not Handled"

        else:
            reply = "Unknown Error"
        Send(reply, address)
                             
            

def run (ip, port):
    sock.bind((ip,port))
    print("Server Listening at: ", sock.getsockname())
    while True:
        data, address = sock.recvfrom(MAX_BYTES)
        ExecuteQuery().run(data,address)  


def Send(data, address):
    reply = "(Server) " + data
    sock.sendto(reply.encode('ascii'), address)

def ClientSignIn(text, address):
    tokens = text.split(' ')
    if len(tokens) == 2:
        if tokens[1] not in Existing:
            return "User: " + tokens[1] + ". Does Not Exist."
        if isOnline(tokens[1], address):
            return "User: " + tokens[1] + ". Is allready Signed in"
        setOnline(tokens[1], address)
        return FetchFile(tokens[1])
        
    else:
        return "Improper SignIn information. Expected format : SignIn <username>"

def ClientHelp():
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
    tokens = text.split(' ')
    message = ""
    if len(tokens) < 2:
        return "Improper use of Send Command. Expected format : Send <username> <message>"
    else:
        message = tokens[1] + " : "
        for i in range(2, len(tokens)):
            message += tokens[i] + " "
    if tokens[1] in Existing:
        senderName = GetClientName(senderAddress)
        if isOnline(tokens[1], 0):
            Found, receiverAddress = GetClientAddress(tokens[1])
            if Found:
                Send(message, receiverAddress)
        else:         
            message = tokens[1] + " is currently offline." + StoreClientMessage(tokens[1],message)
    else:
        message = tokens[1] + " Does not exist!"

    return message
 

def ClientSignOut(addr):
    found = -1
    #get mutex lock on OnLine
    for i in range(0,len(OnLine)):
        if OnLine[i][1] == addr:
            found = i
            break
    if (found != -1):
        del OnLine[found]
        #release mutex
        return "Sign Out successful!"  
    else:
        #release mutex
        return "You can not Sign Out if you have not Signed In"

def StoreClientMessage(user, message):
    try:
        f = open("Clients/"+user, "a")
        f.write(message)
        f.write('\n')
        f.close()
    except IOError:
        return("Error saving Message")
    return "Message successfully saved!"

def FetchFile(username):
    messages = []
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
    reply = "Welcome Back " + username + "! You have " + str(len(messages)) + " new message(s).\n"
    for i in range(0,len(messages)):
        reply += messages[i] 
    return reply

def isOnline(name, address):
    #get OnLine mutex
    Found = False
    for i in range(0,len(OnLine)):
        if name == OnLine[i][0]:
            Found = True
   #release
    return Found
def GetClientName(addr):
    name = ""
    #getonline mutex
    for i in range(0,len(OnLine)):
        if addr == OnLine[i][1]:
            name = OnLine[i][0]
            break   
    #release mutex
    return name

def GetClientAddress(username):
    #get OnLine mutex
    Found = False
    addr = ""
    for i in range(0,len(OnLine)):
        if username == OnLine[i][0]:
            addr = OnLine[i][1]
            Found = True
            break
   #release
    return Found, addr
def setOnline(username, address):
    #get mutex
    OnLine.append([username, address])
    #release mutex
