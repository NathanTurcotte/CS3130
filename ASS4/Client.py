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
    """
        Establish Connection with (host,port)
        format data from list object to string using formatReply
        send the formatted data
        wait for return message
    """
    message = formatReply(data)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((host,port))
    except socket.error:
        print("\nError Connecting to server, Try again later")
        EnterToContinue()
        return
    print("\nRequest Sent")
    try:
        sock.sendall(message.encode('ascii'))
    except socket.error as e:
        print("Error Sending Message :\n", e)
    print("Waiting for reply from Server")
    message = ra.receiveMessage(sock)
    if message is None:
        print("Error Receiving Reply")
    else:
        print("Reply Received\n")
        print(message)
    sock.close()
    EnterToContinue()

def formatReply(data):
    """
        Format a List object into a string to be sent to the server
        ['add','nathan','turcotte','science'] -> "add:nathan:turcotte:science:;"
    
    """
    message = ""
    for i in range(0,len(data)):
        message += data[i] + ":"
    return message + ";"

def client(host,port):
    """
        Prompt the user to make a decision.
        Call the appropriate function to get additional data.
        The called functions will return a list object, or None
    """
    active = True
    request = None
    try:
        while active:
            print(MenuString)
            expectReply = False
            line = input()
            if line == "1":
                print("\nAdd Employee to database")
                request = cdb.AddEmployee()
            elif line == "2":
                print("\nSearch for employee")
                request = cdb.FindEmployee()
            elif line == "3":
                print("\nRemove employee from database")
                request = cdb.RemoveEmployee()
            elif line == "4":
                print("\nDisplay entire database")
                request = cdb.DisplayEmployees()
            elif line == "5":
                active = False
                request = None
            else:
                request = None
                print("Invalid Entry. Try one of the following digits : 1,2,3,4,5")
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
