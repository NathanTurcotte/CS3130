#!/usr/bin/python
import database

#Nathan Turcotte
#CS3130 Assignement#1
#main

MenuString = """
--
Employee FMS
 try:
Select one of the following:
  
  1) Add a new employee
  2) Search for an employee
  3) Remove an employee from FMS
  4) Display entire employee FMS
  5) Quit(Save)
  
--"""

def EnterToContinue():
    print("Press Enter to continue")
    try:
        input()
    except EOFError:
        return

def menu():
    active = True
    try:
        while active:
            print(MenuString)
            line = input()
            if line == '1':
                print("\nAdd Employee to database")
                database.AddEmployee(data)
                EnterToContinue()
            elif line == '2':
                print("\nSearch for employee")
                database.FindEmployee(data)
                EnterToContinue()
            elif line == '3':
                print("\nRemove employee from database")
                database.RemoveEmployee(data)
                EnterToContinue()
            elif line == '4':
                print("\nDisplay entire database")
                database.DisplayEmployees(data)
                EnterToContinue()
            elif line == '5':
                database.SaveDataBase(data)
                active = False
    except EOFError:
        database.SaveDataBase(data)
        return

data = database.ReadDataBase()
menu()
