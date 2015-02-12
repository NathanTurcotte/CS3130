#!/usr/bin/env python3
import socket
import threading
import re
import sys

MAX_BYTES = 65535


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
Alive = True

def run (ip, port):
    """
        Sets up a UDP connection
        Fires a Thread to receive Data, while the main program
        takes care of input
    """
    sock.connect((ip,port))
    sock.send("Help".encode('ascii'))

    receiveThread = ReceiveThread()
    receiveThread.start()
    while True:
        try:
            data = input()
            if data == "Exit":          
                break
            Send(data)
        except EOFError:           
            break;
    #exit


    Send("SignOut")
    print("Thank You for using MMS")
    receiveThread.Alive = False;
    receiveThread.join()
    

    return

class ReceiveThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.Alive = True
    def run(self):
        while self.Alive:
            data = sock.recv(MAX_BYTES)
            Output(data.decode('ascii'))
        sys.exit(0)

def Send(data):      
    """
        Takes a raw string
            encodes it to ascii format
            then sends it over the network
    """
    sock.send(data.encode('ascii'))

def Output(data):
    print(data)
