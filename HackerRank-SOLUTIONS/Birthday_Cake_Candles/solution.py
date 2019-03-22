#!/bin/python3

# Complete the birthdayCakeCandles function below.
def birthdayCakeCandles(ar):
    largest = ar[0]
    for x in range(ar.__len__()):
        if (largest < ar[x]):
            largest = ar[x]

    onlyGreaterEquals = list(filter(lambda x: (x==largest), ar))
    return onlyGreaterEquals.__len__()

ar_count = int(input())

ar = list(map(int, input().rstrip().split()))

result = birthdayCakeCandles(ar)

print(result)