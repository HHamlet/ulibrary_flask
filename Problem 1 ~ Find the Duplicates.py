from typing import Any


def find_duplicates(nums: list) -> list[Any] | None:
    temp = []
    duplicate = set()
    for i in nums:
        if i not in temp:
            temp.append(i)
        else:
            duplicate.add(i)
    if len(duplicate) == 0:
        return None
    else:
        return list(duplicate)


num = [6, 2, 5, 2, 6, 2]
print(find_duplicates(num))
