import requests
import re

WEBSITE = "http://www.theglobeandmail.com/globe-investor/"
MENUSTRING = """
--
Market information

Select one of the following :
    
    1) S&P TSX
    2) S&P 500
    3) Dow Jones
    4) Nasdag
    5) CAD/USD
    6) Gold
    7) WTI Crude
    8) Quit

"""
def extract(data):
    """
        Receives entire html text from webpage
        Extracts required values into a list of list
    """
    #Find all div's/span's with needed values
    value = re.findall("prominent less-prominent(.*?)</div>", data)
    change = re.findall("<div class=\"change\">(.*?)</div>",data)
    time = re.findall("class=\"timing update-info\" (.*?)</span>", data)
    eData = []
    #Extract values from div's/span's, add to a list. Add the list to another once complete
    for i in range(0,len(value)):
        d = []

        r = re.search("[0-9]*,[0-9]*\.[0-9]{2}", value[i])
        if r is None:
            r = re.search("[0-9]{1,}\.[0-9]*", value[i])
        d.append(r.group())
        
        r = re.search("(\-|\+)[0-9]{1,}\.[0-9]{1,}", change[i])
        d.append(r.group())
        
        r = re.search("(\-|\+)[0-9]{1,}\.[0-9]{1,}%", change[i])
        d.append(r.group())

        r = re.search("[0-9]{1,}:[0-9]{2} [A-Z]{2} [A-Z]{3}", time[i])
        d.append(r.group())
        
        eData.append(d)
    return eData
    

def display(index, key):
    """
        print list elements, index(int) indicates type
    """
    string = ""
    if (index == 0) :
        string =   "S&P TSX"
    elif (index == 1) :
        string = "S&P 500"
    elif (index == 2) :
        string = "Dow Jones"
    elif (index == 3) :
        string = "Nasdag"
    elif (index == 4) :
        string = "CAD/USD"
    elif (index == 5) :
        string = "Gold"
    elif (index == 6) :
        string = "WTI Crude"
    else :
        print()
        print("Invalid Entry")
        return
    string += " "
    string += key[0]
    string += " "
    string += key[1]
    string += " "
    string += key[2]
    string += " last updated "
    string += key[3]
    print()
    print(string)

def pressEnter():
    print()
    print("Press Enter to Continue")
    input()

def main():
    r = requests.get(WEBSITE)
    values = extract(r.text)
    keepon = True
    while keepon == True:
        print(MENUSTRING)
        x = input()
        if (x.isdigit()):
            if int(x) > 0 and int(x) < 8:
                display(int(x)-1, values[int(x)-1])
            elif int(x) == 8:
                keepon = False
        pressEnter()
if __name__ == "__main__":
    main()
    






