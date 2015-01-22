#!/usr/bin/python
import sys
import dictionary

for i in range (0,len(sys.argv)):
    if i != 0:    
        dictionary.readFile(sys.argv[i])
