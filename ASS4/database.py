#!user/bin/python
"""
Nathan Turcotte
CS3130 Assignement #4
Server Database interaction module
"""
#database file, if the file does not exist, it will be created
databaseFile = "data.txt"

# Returns a list of dictionaries from a file(name specified by databaseFile above)
def ReadDataBase():
    data = []
    try:
        f = open(databaseFile, 'r')
    except IOError :
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
def AddEmployee(data, tokens):
    valid = False
    if len(tokens) != 6:
        return "Invalid parameters"

    if tokens[1].isdigit():
        pass
    else:
        return "Invalid ID detected"
    if EmployeeExist(data,tokens[1]) == -1:
        pass
    else:
        return "Employee with ID " + tokens[1] + ", already exist"
    
    if tokens[2].isalpha():
        pass
    else:
        return "Invalid First Name"
    if tokens[3].isalpha():
        pass
    else:
        return "Invalid Last Name"
    if tokens[4].isalpha():
        pass
    else:
        return "Invalid Department Name"

    rec = {'id' : tokens[1], 'fname' : tokens[2], 'lname' : tokens[3], 'dep' : tokens[4]}
    data.append(rec)
    SaveDataBase(data)
    return "Employee Successfully Added!"
    
  
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
def FindEmployee(data, tokens):
    if len(tokens) != 3:
        return "Invalid parameters"
    index = EmployeeExist(data,tokens[1])
    if index == -1:
        return "Employee ID does not exist"
    else:
        return "First name : " + data[index]['fname'] + "\nLast name : " + data[index]['lname'] + "\nDepartment : " + data[index]['dep']

#
# Prompts user for an ID number
# If the id exist, the employee will be removed
#
# Also saves dictionaryList back to file using SaveDataBase(list)
#
def RemoveEmployee(data, tokens):
    if len(tokens)!=3:
        return "Invalid Parameters"
    index = EmployeeExist(data,tokens[1])
    if index == -1:
        return "Employee ID does not exist"
    else:
        del data[index]
        return "Employee Successfully Removed"
    SaveDataBase(data)

#
# Display all the employees in the given list of dictionary
#
def DisplayEmployees(data):
    message = ""
    for i in range(0,len(data)):
        message += "ID Number : "  + data[i]['id'] + "\n"
        message += "First name : " + data[i]['fname'] + "\n"
        message += "Last name : "  + data[i]['lname'] + "\n"
        message += "Department : " + data[i]['dep'] + "\n"
        message += "\n"
    return message
        

