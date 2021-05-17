class arithmeticSeq:
    #works with arithmetic sequences

    def __init__(self, a_1, d):
        #save values internally
        self.a_1 = a_1  # inital value in sequence
        self.d = d      # common difference

    def get_nth(self, n):
        nth = self.a_1 + self.d * (n-1)
        return nth

    def get_sum(self, n1, n2):
        total = 0
        for n in range(n1, n2+1):
            a_n = self.get_nth(n)
            total = total + a_n
        return total

# Program starts here

# Set up our specific sequence (instantiate the class)
seq = arithmeticSeq(4, 2)

# Get the 5th value in sequence (use a method from the class)
a_5 = seq.get_nth(5)
print("5th term:", a_5)

# Find the sum of the first four values in the sequence
sum = seq.get_sum(1, 4)
print("Sum of first 5 terms:", sum)
