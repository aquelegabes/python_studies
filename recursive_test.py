def Factorial(number):
	if (number == 1):
		return 1
	else:
		return number * Factorial(number -1)

def OneLinerFactorial(number):
	return 1 if number == 1 else number * Factorial(number - 1)
	
print(Factorial(5))
