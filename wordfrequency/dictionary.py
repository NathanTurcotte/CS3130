#Nathan Turcotte
#5027975
#Dictionary Module


#Attempts to open file given as parameter
#If the file does not exist, the function simply returns and outputs nothing
def readFile(fileName):
    try:
        file = open(fileName, 'r')
    except Exception:
        print("Error opening file")
        return
#read the complete file as one string
    contents = file.read()
    c = ""
#go through the entire string, replacing any non alphabetic characters with " "
    for i in range(0,len(contents)):
        if contents[i].isalpha() :
            c = c+contents[i] 
        else:
            c = c + " " 
#string unneccessary white space on the extremities, then split the string on white space 
    c = c.strip().split()
#data and count will hold the processed data
    data  = []
    count = []
#for each word in c, check if it has been processed, if so, increment the count. otherwise create the entry
    for i in range(0,len(c)):
        c[i] = c[i].lower()
        new = True
        for j in range(0,len(data)):
            if data[j] == c[i]:
                count[j] = count[j]+1
                new = False
        if new:
            data.append(c[i])
            count.append(1)
#Go through data and count. print results
    print("Word Frequency                    | Histogram")
    print("----------------------------------------------")
    for i in range(0,len(data)):
        print("%-25.25s  %-5.5i  |%s" % (data[i],count[i],histoString(count[i])))

#prints the appropriate histogram line of the given count
def histoString(count):
    string = "{0:x<{c}}".format("",c=min(count,10))
    if (count-10 > 0):
        string += "({})".format(str(count-10))
    return string                          
        
