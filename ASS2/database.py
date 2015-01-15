#!user/bin/python


databaseFile = "data.txt"

def ReadDataBase():
    dictionaryList = []
    try:
        f = open(databaseFile, 'r')
    except IOError:
        return dictionaryList
    
    data = f.readlines()
    for line in data:
        AddRecord(line,dictionaryList)
    f.close()
    return dictionaryList
            

def AddRecord(line, dictionaryList):
    tmp = line.strip()
    tmp = tmp.split(':')
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
        dictionaryList.append(record)

def SaveDataBase(list):
    f = open(databaseFile, 'w')
    for i in range(0,len(list)):
        f.write(list[i]['id'])
        f.write(':')
        f.write(list[i]['fname'])
        f.write(':')
        f.write(list[i]['lname'])
        f.write(':')
        f.write(list[i]['dep'])
        f.write('\n')
    f.close()
    
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
    print("New Employee(", rec, ") successfully added!")
    
def EmployeeExist(data,id):
    exist = -1
    for l in range(0,len(data)):
        if data[l]['id'] == id:
            exist = l
            break
    return exist

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

def DisplayEmployees(data):
    for i in range(0,len(data)):
        print("ID Number : ", data[i]['id'])
        print("First name : ",data[i]['fname'])
        print("Last name : ",data[i]['lname'])
        print("Department : ",data[i]['dep'])
        print("")
        

