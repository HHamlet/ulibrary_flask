def euclidean_algo_gcd(x, y):
    while y:
        x, y = y, x % y
    return abs(x)


def GCD(x: int, y: int, z: int):
    if z != 0:
        tempdev = euclidean_algo_gcd(x, y)
        return euclidean_algo_gcd(tempdev, z)
    else:
        return euclidean_algo_gcd(x, y)


print(GCD(24, 36, 16))
