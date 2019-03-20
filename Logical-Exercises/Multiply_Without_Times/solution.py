def MultiplyRecursive(num, times):
    result = num
    if (times == 0):
        return 0
    if (times == 1):
        return num
    return (result + MultiplyRecursive(num, times-1))

def Multiply(num, times):
    if (times == 0):
        return 0
    result = num
    for index in range(1, times):
        result += num
    return result


print(Multiply(2,5))