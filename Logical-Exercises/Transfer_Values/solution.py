def TransferValues1(num1, num2):
    num1[0] = num1[0] + num2[0]
    num2[0] = num1[0] - num2[0]
    num1[0] = num1[0] - num2[0]

def TransferValues2(num1, num2):
    num1[0] ^= num2[0]
    num2[0] ^= num1[0]
    num1[0] ^= num2[0]

a = [4]
b = [6]

TransferValues1(a, b)
print (a,b)