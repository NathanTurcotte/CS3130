MAX_BYTES = 65535

import socket
import ra
import database
import ssl

cafile = "ca.crt"
certfile = "localhost.pem"


def server(host, port) :
    """
        Bind and listen on socket
    """
    data = database.ReadDataBase()
    mess = "hello from server;"   
    #NEW!
    purpose = ssl.Purpose.CLIENT_AUTH
    context = ssl.create_default_context(purpose)
    context.load_cert_chain(certfile)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    sock.bind((host,port))
    sock.listen(1)
    print('Listening at : ', sock.getsockname)
    while True:
        try:
            soc, sockname = sock.accept()
            #NEW!
            sc = context.wrap_socket(soc,server_side=True)
            print('Connection accepted')
        except socket.error:
            print("Error accepting Connection")
        message = ra.receiveMessage(sc)
        if message is None:
            print("Error Receiving message")
            sc.close()
            continue
        print("Message received from client : ", message)
        message = execute(data,message) + ";"
        print("Sending back : ", message)
        try:
            sc.sendall(message.encode('ascii'))
        except socket.error as e:
            print("Error Sending Message ", e)
        sc.close()
        
def execute(data,message):
    """
        Take the string received from the Client
        Split the string on ':'
        Call the appropriate database function which returns a string to be sent back to the client
    """
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
