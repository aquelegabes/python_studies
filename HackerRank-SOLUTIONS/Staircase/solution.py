#!/bin/python3

import os

# Complete the staircase function below.
def staircase(n):
    #Counter weighting n by +1, because we're starting at x = 1 
    for x in range(1,n+1):
        spaces = n-x
        string = ""
        for i in range(0,spaces):
            string += " "
        while (string.__len__() < n):
            string += "#"
        print(string)

staircase(6)