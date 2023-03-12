def twoSum(nums: list[int], target: int) -> list[int]:
    i = 0
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[j] == target - nums[i]:
                return [i, j]


def twosum_heshmap(nums: list[int], target: int):
    hashmap = {}
    for i in range(len(nums)):
        complement = target - nums[i]
        if complement in hashmap:
            return [i, hashmap[complement]]
        hashmap[nums[i]] = i


nums = [1, 5, 3, 1, 5, 1]
target = 12
print(twoSum(nums, target))
print(twosum_heshmap(nums, target))
