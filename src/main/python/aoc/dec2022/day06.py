from aoc.common.day_solver import DaySolver


class Day06Solver(DaySolver):
    year = 2022
    day = 6

    def solve_puzzle_one(self):
        return self._find_unique_of_length(4)

    def solve_puzzle_two(self):
        return self._find_unique_of_length(14)

    def _find_unique_of_length(self, length):
        line = self.load_only_input_line()
        for i in range(len(line) - length):
            chars = set(line[i:i+length])
            if len(chars) == length:
                return i + length

        return 'ERROR'
