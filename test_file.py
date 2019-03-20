def Factorial(number):
	if (number == 1):
		return 1
	else:
		return number * Factorial(number -1)

print(Factorial(5))