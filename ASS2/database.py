#!user/bin/python

#Nathan Turcotte
#CS3130 Assignement #1
#Database interaction module

#database file, if the file does not exist, it will be created
databaseFile = "data.txt"

# Returns a list of dictionaries from a file(name specified by databaseFile above)
def ReadDataBase():
    data = []
    try:
        f = open(databaseFile, 'r')
    except IOErro :
        return data
    
    contents = f.readlines()
    for line in contents:
        AddRecord(line,data)
    f.close()
    return data
            
#
# Splits the given line into a dictionary.
# Adds the dictionary to a list specified by the second argument
# The line must contain exactly 4 elements
# ID number must contain only digits
# First name, last name and department must contain only alphabetical letters
# The line is ignored if any of these conditions fail
# 

def AddRecord(line, data):
    line = line.strip()
    tmp = line.split(':')
    valid = True
    if len(tmp) == 4:
        if tmp[0].isdigit() == False:
            valid = False
        elif tmp[1].isalpha() == False:
            valid = False
        elif tmp[2].isalpha() == False:
            valid = False
        elif tmp[3].isalpha() == False:
            valid = False
    else :
        valid = False
    if valid:
        record = {'id':tmp[0] , 'fname':tmp[1], 'lname':tmp[2], 'dep':tmp[3]}
        data.append(record)
#
# Rewrites the file specified by databaseFile
#
def SaveDataBase(data):
    f = open(databaseFile, 'w')
    for i in range(0,len(data)):
        f.write(data[i]['id'])
        f.write(':')
        f.write(data[i]['fname'])
        f.write(':')
        f.write(data[i]['lname'])
        f.write(':')
        f.write(data[i]['dep'])
        f.write('\n')
    f.close()
   
#
# Prompts user to enter appropriate fields to create an employee. 
# Creates a proper dictionary with the given data
# And adds it to a list passed as the parameter data
# 
# Also saves dictionaryList back to file using SaveDataBase(list)
#
def AddEmployee(data):
    valid = False
    try:
        while valid == False:
            print("ID Number : ",end="")
            id = input()
            if id.isdigit():
                if EmployeeExist(data,id) == -1:
                    valid = True
                else:
                    print("Given ID allready exist")
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
        return
    rec = {'id' : id, 'fname' : fname, 'lname' : lname, 'dep' : dep}
    data.append(rec)
    print("New Employee successfully added!\n")
    SaveDataBase(data)
  
#
# Searches through the parameter data,
# for a dictionary with id field equals to parameter id
# returns index of the employee if they exist
# returns -1 otherwise
#  
def EmployeeExist(data,id):
    exist = -1
    for l in range(0,len(data)):
        if data[l]['id'] == id:
            exist = l
            break
    return exist

#
# Prompts user for an ID number
# Searches through parameter data
# for the given employee.
# If found, print the employees data
#
def FindEmployee(data):
    print("ID number : ", end="")
    try:
        id = input()
    except EOFError:
        return
    index = EmployeeExist(data,id)
    if index == -1:
        print("Employee ID does not exist")
    else:
        print("First name : ",data[index]['fname'])
        print("Last name : ",data[index]['lname'])
        print("Department : ",data[index]['dep'])
    print("")
#
# Prompts user for an ID number
# If the id exist, the employee will be removed
#
# Also saves dictionaryList back to file using SaveDataBase(list)
#
def RemoveEmployee(data):
    print("ID number : ", end="")
    try:
        id = input()
    except EOFError:
        return
    index = EmployeeExist(data,id)
    if index == -1:
        print("Employee ID does not exist")
    else:
        del data[index]
        print("Employee successfully removed")
        print("")
    SaveDataBase(data)

#
# Display all the employees in the given list of dictionary
#
def DisplayEmployees(data):
    for i in range(0,len(data)):
        print("ID Number : ", data[i]['id'])
        print("First name : ",data[i]['fname'])
        print("Last name : ",data[i]['lname'])
        print("Department : ",data[i]['dep'])
        print("")
    print("")
        

