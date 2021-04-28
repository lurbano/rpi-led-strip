

def decimalToBinary(decimalNumber):
    binaryString = ""
    while decimalNumber >= 1:
        binaryString += str(decimalNumber % 2)
        decimalNumber = decimalNumber // 2
    binaryString = binaryString[::-1]
    print(binaryString)

for i in range(10):
    print(i)
    decimalToBinary(i)
