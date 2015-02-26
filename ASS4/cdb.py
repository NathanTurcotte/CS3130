"""
    The functions of this Module collect data from the user.
    Format the data into a list
        ["<action>", <element1>, <element2>, <elementn>]
    then return the list
"""

def AddEmployee():
    """
        Promps and Validates data from user.
    """
    valid = False
    try:
        while valid == False:
            print("ID Number : ",end="")
            id = input()
            if id.isdigit():
                valid = True
            else:
                print ("Invalid ID")
        valid = False
        while valid == False:
            print("First Name : ",end="")
            fname = input()
            if fname.isalpha():
                valid = True
            else:
                print ("Invalid First Name")
        valid = False
        while valid == False:
            print("Last Name : ",end="")
            lname = input()
            if lname.isalpha():
                valid = True
            else:
                print ("Invalid Last Name")
        valid = False
        while valid == False:
            print("Department Name : ",end="")
            dep = input()
            if dep.isalpha():
                valid = True
            else:
                print ("Invalid Department Name")
    except EOFError:
        return None 
    return  ["add", id, fname, lname, dep]

def FindEmployee():
    """
        prompts user for id number
    """
    print("ID number : ", end="")
    try:
        id = input()
    except EOFError:
        return None
    return ["find", id]

def RemoveEmployee():
    """
        prompts user for id number
    """
    print("ID number : ", end="")
    try:
        id = input()
    except EOFError:
        return None
    return ["remove", id]

def DisplayEmployees():
    return ["display"]


    
