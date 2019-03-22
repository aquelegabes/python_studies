#!/bin/python3
import os

# Complete the miniMaxSum function below.
def miniMaxSum(arr):
    arr.sort()
    min = 0
    max = 0
    for x in range(1,arr.__len__()):
        max += arr[x]
    for x in range(0,arr.__len__()-1):
        min += arr[x]

    print (min, max)

arr = [6,2,0,4,7]

miniMaxSum(arr)