#!/bin/python3

import os
import sys

# Complete the twoStrings function below.
def twoStrings(s1, s2):
    result = "NO"
    for char in s1:
        if s2.__contains__(char):
            result = "YES"
            break
    return result

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    q = int(input())

    for q_itr in range(q):
        s1 = input()

        s2 = input()

        result = twoStrings(s1, s2)

        fptr.write(result + '\n')

    fptr.close()