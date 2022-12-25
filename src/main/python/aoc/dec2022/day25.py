from aoc.common.day_solver import DaySolver

CHAR_TO_VALUE = {'=': -2, '-': -1, '0': 0, '1': 1, '2': 2}
VALUE_TO_CHAR = {0: '=', 1: '-', 2: '0', 3: '1', 4: '2'}


class Day25Solver(DaySolver):
    year = 2022
    day = 25

    def solve_puzzle_one(self):
        lines = self.load_all_input_lines()

        total = 0
        for line in lines:
            for i, c in enumerate(line[::-1]):
                total += CHAR_TO_VALUE[c] * (5 ** i)

        result = ''
        while total:
            total, rem = divmod(total + 2, 5)
            result = VALUE_TO_CHAR[rem] + result

        return result

    def solve_puzzle_two(self):
        return 'ALL DONE!'
