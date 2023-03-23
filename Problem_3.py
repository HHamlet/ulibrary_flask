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


def GCD_1(*args: int):
    if len(args) >= 2:
        temp_gcd = euclidean_algo_gcd(args[0], args[1])
        ind = 1
        while ind != len(args) - 1:
            ind += 1
            temp_div = euclidean_algo_gcd(temp_gcd, args[ind])
            temp_gcd = temp_div
        return temp_gcd
    else:
        return f"Missing some arguments."


print(GCD(24, 36, 16, 8, 7))
print(GCD_1(24, 36, 16, 8, 4))
