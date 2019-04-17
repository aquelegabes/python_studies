#!/bin/python3

import re

#
# Complete the timeConversion function below.
#
def CheckForCorrectStringStamp(text):
    pattern = "am|pm"
    match = re.search(pattern,text,re.I)    
    return match.group(0)    

def correctHours(timestamp, time):
    match = re.search("pm",timestamp,re.I)
    after2digits = time[2:]
    if (match and match.group(0)):
        if int(time[:2]) == 12:
            return "12%s" % (after2digits)
        elif int(time[:2]) == 1:
            return "13%s" % (after2digits)
        elif int(time[:2]) == 2:
            return "14%s" % (after2digits)
        elif int(time[:2]) == 3:
            return "15%s" % (after2digits)
        elif int(time[:2]) == 4:
            return "16%s" % (after2digits)
        elif int(time[:2]) == 5:
            return "17%s" % (after2digits)
        elif int(time[:2]) == 6:
            return "18%s" % (after2digits)
        elif int(time[:2]) == 7:
            return "19%s" % (after2digits)
        elif int(time[:2]) == 8:
            return "20%s" % (after2digits)
        elif int(time[:2]) == 9:
            return "21%s" % (after2digits)
        elif int(time[:2]) == 10:
            return "22%s" % (after2digits)
        elif int(time[:2]) == 11:
            return "23%s" % (after2digits)
    else:
        if int(time[:2]) == 12:
            return "00%s" % (after2digits)
        return time

def timeConversion(s):
    if(CheckForCorrectStringStamp(s)):
        # obtaining only the format (PM/AM)
        timestamp = s[-2:]
        # removing PM/AM from string
        s = s[:-2]
        return correctHours(timestamp,s)
    else:
        return (s[:-2])

s = "12:48:31AM"
result = timeConversion(s)
print (result)
