def Multiply(num, times):
    if (times == 0):
        return 0
    result = num
    for index in range(1, times):
        result += num
    return result

def MultiplyRecursive(num, times):
	if (times == 0):
		return 0
	return num + MultiplyRecursive(num, times - 1)

print(Multiply(2,5))
