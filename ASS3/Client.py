#!/usr/bin/env python3
import socket
import threading
import re

MAX_BYTES = 65535


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def run (ip, port):
    sock.connect((ip,port))
    sock.send("Help".encode('ascii'))
    inputThread = InputThread()
    inputThread.start()
    receiveThread = ReceiveThread()
    receiveThread.start()
    while True:
        x = 5

class InputThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:    
            Send(input())


class ReceiveThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        while True:
            data = sock.recv(MAX_BYTES)
            Output(data.decode('ascii'))

def Send(data):      
    sock.send(data.encode('ascii'))

def Output(data):
    print(data)
