def get_nth(a_1, d, n):
    nth = a_1 + d * (n-1)
    return nth

def get_sum(a_1, d, n1, n2):
    total = 0
    for n in range(n1, n2+1):
        a_n = get_nth(a_1, d, n)
        total = total + a_n
    return total

sum = get_sum(4, 2, 3, 50)
print("Sum from 3 to 50 =", sum)
