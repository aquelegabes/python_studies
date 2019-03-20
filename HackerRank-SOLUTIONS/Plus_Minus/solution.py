#!/bin/python3
import os

# Complete the plusMinus function below.
def plusMinus(arr):
    size = float(arr.__len__())
    positives = 0
    negatives = 0
    zeros = 0
    for value in arr:
        if (value > 0):
            positives += 1.0
        elif (value < 0):
            negatives += 1.0
        else:
            zeros += 1.0
    print (positives/size)
    print (negatives/size)
    print (zeros/size)

if __name__ == '__main__':
    n = int(input())

    arr = list(map(int, input().rstrip().split()))

    plusMinus(arr)
