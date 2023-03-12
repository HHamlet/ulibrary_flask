def euclidean_algo_gcd(x, y):
    while y:
        x, y = y, x % y
    return abs(x)


def GCD(x: int, y: int, *args: int):
    if args != 0:
        eag = euclidean_algo_gcd(x, y)
        for el in args:
            tempdev = euclidean_algo_gcd(eag, el)
            eag = tempdev
        return eag
    else:
        return euclidean_algo_gcd(x, y)


print(GCD(24, 36, 16, 8, 7))
