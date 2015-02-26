#!/usr/bin/env python3
import socket
import cdb
import ra
import re

MenuString = """
--
Employee FMS
Select one of the following:
  
  1) Add a new employee
  2) Search for an employee
  3) Remove an employee from FMS
  4) Display entire employee FMS
  5) Quit
  
--"""

def send(host, port, data):
    message = formatReply(data)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host,port))
    print("\nRequest Sent")
    sock.sendall(message.encode('ascii'))
    print("Waiting for reply from Server")
    message = ra.receiveMessage(sock)
    if message is None:
        print("Error Receiving Reply")
    else:
        print("Reply Received")
        print(message)
    sock.close()
    EnterToContinue()

def formatReply(data):
    """
        Format a List object into a string to be sent to the server
    
    """
    message = ""
    for i in range(0,len(data)):
        message += data[i] + ":"
    return message + ";"

def client(host,port):
    active = True
    request = None
    try:
        while active:
            print(MenuString)
            expectReply = False
            line = input()
            if line == '1':
                print("\nAdd Employee to database")
                request = cdb.AddEmployee()
            elif line == '2':
                print("\nSearch for employee")
                request = cdb.FindEmployee()
            elif line == '3':
                print("\nRemove employee from database")
                request = cdb.RemoveEmployee()
            elif line == '4':
                print("\nDisplay entire database")
                request = cdb.DisplayEmployees()
            elif line == '5':
                active = False
            if request is None:
                pass
            else:
                send(host, port, request)
    except EOFError:     
        return

def EnterToContinue():
    print("\nPress Enter to continue")
    try:
        input()
    except EOFError:
        return
