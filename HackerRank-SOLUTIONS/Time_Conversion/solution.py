#!/bin/python3

import re

#
# Complete the timeConversion function below.
#
def CheckForCorrectStringStamp(text):
    textLength = len(text)
    lastChars = text[-2:]
    pattern = r"'am|pm'gmi"
    match = re.search(pattern,text)
    print (match)
    

def timeConversion(s):
    if(CheckForCorrectStringStamp(s)):
        return "lol"

s = "08:48:31PM"
result = timeConversion(s)
print (result)
