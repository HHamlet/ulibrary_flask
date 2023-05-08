import random
import math


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
]

solved_puzzle = [
    [1, 2, 3, 4, 5, 6, 7, 8, 9],
    [4, 5, 6, 7, 8, 9, 1, 2, 3],
    [7, 8, 9, 1, 2, 3, 4, 5, 6],
    [2, 1, 4, 3, 6, 5, 8, 9, 7],
    [3, 6, 5, 8, 9, 7, 2, 1, 4],
    [8, 9, 7, 2, 1, 4, 3, 6, 5],
    [5, 3, 1, 6, 7, 2, 9, 4, 8],
    [6, 7, 2, 9, 4, 8, 5, 3, 1],
    [9, 4, 8, 5, 3, 1, 6, 7, 2]
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


class SudokuBoard:
    def __init__(self, initialPuzzle):

        self.puzzle = []
        for row in initialPuzzle:
            _row = []
            for value in row:
                _row.append(SudokuCell(value, value != 0))
            self.puzzle.append(_row)
        self.size = len(self.puzzle)

    def print_board(self):
        for i, row in enumerate(self.puzzle):
            print_str = ""
            for j, cell in enumerate(row):
                print_str += f"{str(cell)}\t"
            print(print_str)

    def checkIfValueIsOk(self, i, j):
        value = self.puzzle[i][j].value
        for k, row in enumerate(self.puzzle):
            if self.puzzle[i][k].value == value and k != j:
                print("Value in row")
                return False
            if self.puzzle[k][j].value == value and k != i:
                print("Value in column")
                return False

        box_size = int(math.sqrt(self.size))

        # cell (4, 7)
        # i = 4; (4 // 3) * 3  -> 3
        # j = 7; (7 // 3) * 3 ->  6

        for k in range((i // box_size) * box_size, (i // box_size) * box_size + box_size):
            for l in range((j // box_size) * box_size, (j // box_size) * box_size + box_size):
                if self.puzzle[k][l].value == value and k != i and l != j:
                    print("Value in small grid")
                    return False

        return True

    def checkIfIsSolved(self):
        for i, row in enumerate(self.puzzle):
            for j, cell in enumerate(row):
                if cell.value == 0:
                    return False
                if not self.checkIfValueIsOk(i, j):
                    return False

        return True

    @classmethod
    def check_possibility(cls, i, j, n):
        for el in range(9):
            if initial_puzzle[i][el] == n:
                return False
        for el in range(9):
            if initial_puzzle[el][j] == n:
                return False
        y = (i // 3) * 3
        x = (j // 3) * 3

        for e in range(3):
            for f in range(3):
                if initial_puzzle[y + e][x + f] == n:
                    return False
        return True

    @classmethod
    def solution(cls, puzzle):
        temp_puzzle = puzzle
        for i in range(9):
            for j in range(9):
                if temp_puzzle[i][j] == 0:
                    for n in range(1, 10):
                        if cls.check_possibility(i, j, n):
                            temp_puzzle[i][j] = n
                            cls.solution(puzzle)
                            temp_puzzle[i][j] = 0
                    return
        cls.__board_print(temp_puzzle)
        input("other solution:")

    @classmethod
    def bord_generator(cls, puzzle, difficulty):
        choices = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        puzzle = solved_puzzle

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
        cls.__board_print(puzzle)
        return puzzle

    @classmethod
    def __board_print(cls, puzzle):
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

# print(board.check_possibility(0, 7, 8))
# SudokuBoard.solution(initial_puzzle)
SudokuBoard.bord_generator(solved_puzzle, "hard")
