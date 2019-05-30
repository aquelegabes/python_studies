def Factorial(number):
	if (number == 1 or number == 0):
		return 1
	else:
		return number * Factorial(number -1)

def OneLinerFactorial(number):
	return 1 if num == 1 or num == 0 else num * Factorial(num - 1)
	
print(Factorial(5))
