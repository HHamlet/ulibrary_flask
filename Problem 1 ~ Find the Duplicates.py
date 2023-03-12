def find_duplicates(num: list):
    duplicate = set()
    for i in num:
        if num.count(i) > 1:
            duplicate.add(i)
    print(*duplicate, sep=",")
    return


num = [6, 2, 5, 2, 6, 2]
find_duplicates(num)
