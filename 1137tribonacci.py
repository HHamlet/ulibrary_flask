from functools import cache


class Solution:
    # recursive solution
    @cache
    def tribonacci(self, n: int) -> int or None:
        if n < 0:
            return None
        elif n == 0:
            return 0
        elif n == 1 or n == 2:
            return 1
        return self.tribonacci(n - 3) + self.tribonacci(n - 2) + self.tribonacci(n - 1)
    # linear solution
    # def tribonacci(self, n: int) -> int:
    # trib = {}
    # trib[0] = 0
    # trib[1] = 1
    # trib[2] = 1
    # i = 3
    # while i <= n:
    #     trib[i] = trib[i - 3] + trib[i - 2] + trib[i - 1]
    #     i +=1
    # return trib[n]


s = Solution()
print(s.tribonacci(135))
