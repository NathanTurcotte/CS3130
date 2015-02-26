import socket
import random
import sys
import time

timeout = 3

def receiveMessage(sock):
    """
        Receive Message. All messages end with a ;
    """
    data = b'' 
    try:
        while True:
            sock.settimeout(timeout)
            more = sock.recv(1)
            if more.decode('ascii') == ';':
                return data.decode('ascii')
            else:
                data += more
    except socket.timeout:
        return None
    except socket.error:
        return None
        
