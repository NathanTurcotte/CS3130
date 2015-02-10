#!/usr/bin/python
import re
""""
    Nathan Turcotte
    5027975
    Lab Assignment #2
    Validate Phone Number Format
    (xxx) xxx-xxxx
    (xxx) xxx xxxx
    (xxx)xxx-xxxx
    (xxx)xxx xxxx
    xxx-xxx-xxxx
    xxx xxx-xxxx
    xxx-xxx xxxx
    xxx xxx xxxx
    xxxxxxxxxx
"""

def process(data):
    """
        determines if a number found in data is valid
    """
    number = re.match(r'((\([\d]{3}\)[ ]{0,1}|[\d]{3} |[\d]{3}-)[\d]{3}[- ][\d]{4})|[\d]{10}', data, 0)
    if number:
        PrintNumber(number.group())
    else:
        print("Invalid Phone Number")
def PrintNumber(data):
    """
        Prints a phone number, assumes the number has 10 valid digits
        remove any non digit
    """
    number = re.sub(r'\D', "", data)
    print("Number is: ", "({}) {} {}".format(number[0:3], number[3:6], number[6:10]))
while True:
    print("Enter a Phone Number: ", end="")
    number = input()
    if number:
        process(number)
    else:
        break
        


