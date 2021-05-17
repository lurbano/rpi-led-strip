def get_nth(a_1, d, n):
    nth = a_1 + d * (n-1)
    return nth

total = 0
for n in range(3, 51):
    a_n = get_nth(4, 2, n)
    total = total + a_n
    print(n, a_n, total)
print("Sum = ", total)
