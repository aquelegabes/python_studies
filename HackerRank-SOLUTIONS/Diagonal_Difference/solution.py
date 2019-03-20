#!/bin/python3

import math
import os

def getPrimaryD(arr, size):
    result = 0
    index = 0
    while (index < size+1):
        result += arr[index][index]
        index += 1
    return result

def getSecondaryD(arr, size):
    result = 0
    outindex = 0
    insideindex = size
    while (outindex < size+1):
        result += arr[outindex][insideindex]
        outindex += 1
        insideindex -= 1
    return result

# Complete the diagonalDifference function below.
def diagonalDifference(arr):
    size = arr.__len__() - 1
    primaryD = getPrimaryD(arr, size)
    secondaryD = getSecondaryD(arr, size)
    return (int)(math.fabs(primaryD - secondaryD))

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    n = int(input())

    arr = []

    for _ in range(n):
        arr.append(list(map(int, input().rstrip().split())))

    result = diagonalDifference(arr)

    fptr.write(str(result) + '\n')

    fptr.close()
