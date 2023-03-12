def euclidean_algo_gcd(x, y):
    while y:
        x, y = y, x % y
    return abs(x)


def GCD(x: int, y: int, *args: int):
    if len(args) > 0:
        temp_gcd = euclidean_algo_gcd(x, y)
        for el in args:
            temp_div = euclidean_algo_gcd(temp_gcd, el)
            temp_gcd = temp_div
        return temp_gcd
    else:
        return euclidean_algo_gcd(x, y)


print(GCD(24, 36, 16, 8, 7))
