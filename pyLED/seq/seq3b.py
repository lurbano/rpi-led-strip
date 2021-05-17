def get_nth(a_1, d, n):
    nth = a_1 + d * (n-1)
    return nth

for n in range(1, 11):
    a_n = get_nth(3, 4, n)
    print(n, "-->", a_n)
