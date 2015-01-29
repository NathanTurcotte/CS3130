#Nathan Turcotte
#5027975
#Assignment #2 Main
#Processes given files, passed by command line arguments, printing word count and histograms.

import sys
import dictionary

for i in range (0,len(sys.argv)):
    if i != 0:    
        print("Processing File : ", sys.argv[i])
        dictionary.readFile(sys.argv[i])
        print()
