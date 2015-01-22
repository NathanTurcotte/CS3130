import string

def readFile(fileName):
    try:
        file = open(fileName, 'r')
    except Exception:
        print("Error opening file")
        return
    contents = file.read()
    c = ""
    for i in range(0,len(contents)):
        if contents[i].isalpha() :
            c = c+contents[i] 
        else:
            c = c + " "  
    c = c.split()
    print(c)
