MAX_BYTES = 65535

import socket
import ra
import database

data = database.ReadDataBase()

def server(host, port) :
    mess = "hello from server;"   
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    sock.bind((host,port))
    sock.listen(1)
    print('Listening at : ', sock.getsockname)
    while True:
        sc, sockname = sock.accept()
        print('Connection accepted')
        message = ra.receiveMessage(sc)
        if message is None:
            print("Error Receiving message")
            sc.close()
            continue
        print("Message received from client : ", message)
        message = execute(message) + ";"
        print("Sending back : ", message)
        sc.sendall(message.encode('ascii'))
        sc.close()
        
def execute(message):
    tokens = message.split(':')
    if not tokens:
        return "Invalid Query"
    if len(tokens) < 1:
        return "Invalid Query"
    if tokens[0] == "add":
        return database.AddEmployee(data, tokens)
    elif tokens[0] == "find":
        return database.FindEmployee(data, tokens)
    elif tokens[0] == "remove":
        return database.RemoveEmployee(data, tokens)
    elif tokens[0] == "display":
        return database.DisplayEmployees(data)
