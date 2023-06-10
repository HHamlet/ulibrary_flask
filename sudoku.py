import random
from collections import defaultdict


class SudokuCell:
    def __init__(self, value, fixed):
        self.value = value
        self.fixed = fixed

    def __str__(self):
        return f"{self.value}"

    def __repr__(self):
        return f"SudokuCell({self.value}, {self.fixed})"


initial_puzzle = [
    [4, 0, 0, 2, 6, 9, 0, 0, 0],
    [6, 8, 2, 0, 7, 1, 0, 9, 3],
    [1, 0, 7, 8, 3, 4, 5, 6, 2],
    [0, 2, 6, 0, 0, 0, 0, 4, 7],
    [3, 0, 4, 6, 8, 2, 9, 1, 5],
    [9, 0, 1, 7, 4, 3, 0, 2, 8],
    [5, 1, 9, 0, 2, 6, 0, 0, 4],
    [2, 4, 0, 9, 5, 7, 1, 3, 6],
    [7, 6, 3, 4, 1, 0, 2, 5, 9]

    # [5, 3, 0, 0, 7, 0, 0, 0, 0],
    # [6, 0, 0, 1, 9, 5, 0, 0, 0],
    # [0, 9, 8, 0, 0, 0, 0, 6, 0],
    # [8, 0, 0, 0, 6, 0, 0, 0, 3],
    # [4, 0, 0, 8, 0, 3, 0, 0, 1],
    # [7, 0, 0, 0, 2, 0, 0, 0, 6],
    # [0, 6, 0, 0, 0, 0, 2, 8, 0],
    # [0, 0, 0, 4, 1, 9, 0, 0, 5],
    # [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

empty_puzzle = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]
]
values = [1, 2, 3, 4, 5, 6, 7, 8, 9]
random.shuffle(values)


class SudokuBoard:
    def __init__(self, initialPuzzle):
        self.my_puzzle = initialPuzzle

    def check_possibility(self, i, j, n):
        for el in range(9):
            if self.my_puzzle[i][el] == n and el != j:
                return False
        for el in range(9):
            if self.my_puzzle[el][j] == n and el != i:
                return False
        y = (i // 3) * 3
        x = (j // 3) * 3

        for e in range(3):
            for f in range(3):
                if self.my_puzzle[y + e][x + f] == n and (y + e != i and x + f != j):
                    return False
        return True

    def find_empty(self):
        for i in range(len(self.my_puzzle)):
            for j in range(len(self.my_puzzle[0])):
                if self.my_puzzle[i][j] == 0:
                    return i, j
        return None

    def solution(self):
        find = self.find_empty()
        if not find:
            return self.my_puzzle
        row, colum = find
        for n in values:
            if self.check_possibility(row, colum, n):
                self.my_puzzle[row][colum] = n
                if self.solution():
                    return self.my_puzzle
                self.my_puzzle[row][colum] = 0

        return False

    @classmethod
    def bord_generator(cls, difficulty):
        choices = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        new_bord = SudokuBoard(empty_puzzle)
        puzzle = new_bord.solution()

        def __add_zero(dif_num):
            count = 0
            while count != dif_num:
                if puzzle[random.choice(choices)][random.choice(choices)] != 0:
                    puzzle[random.choice(choices)][random.choice(choices)] = 0
                    count += 1
            return puzzle

        if difficulty.lower() == "hard" or difficulty == "3":
            dif = 81 // 4
            puzzle = __add_zero(dif)
        elif difficulty.lower() == "medium" or difficulty == "2":
            dif = 81 // 2
            puzzle = __add_zero(dif)
        elif difficulty.lower() == "easy" or difficulty == "1":
            dif = (81 * 3) // 4
            puzzle = __add_zero(dif)
        print("New Puzzle generated...")
        cls.board_print(puzzle)
        return puzzle

    @classmethod
    def board_print(cls, puzzle):
        for i, row in enumerate(puzzle):
            if i % 3 == 0:
                print(13 * "-\t")
            print_str = ""
            for j, cell in enumerate(row):
                if j % 3 == 0:
                    print_str += "|\t"

                print_str += f"{str(cell)}\t"
            print_str += "|\t"
            print(print_str)
        print(13 * "-\t")


board = SudokuBoard(initial_puzzle)
board1 = SudokuBoard(empty_puzzle)
# board.print_board()
# board1.print_board()
# print(board1.check_possibility(empty_puzzle, 0, 7, 8))
# board1.solution()
# solved = board.solution()
# solved1 = board1.solution()
# board.board_print(board.my_puzzle)
# board1.board_print(board1.my_puzzle)
puzzle1 = SudokuBoard.bord_generator("hard")
board2 = SudokuBoard(puzzle1)
board2.board_print(board2.solution())
