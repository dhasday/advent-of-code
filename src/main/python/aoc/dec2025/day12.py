import operator

from aoc.common import helpers
from aoc.common.day_solver import DaySolver


class Day12Solver(DaySolver):
    year = 2025
    day = 12

    def solve_puzzle_one(self):
        """
        The naive check of total presents size vs region area produces the correct result
        and based on the part 2 hover text appears to be the intended solution for this one.
        """
        lines = self.load_all_input_lines()

        present_sizes = list()
        for idx in range(0, 30, 5):
            cur_size = 0
            for line in lines[idx + 1:idx + 4]:
                for val in line:
                    if val == '#':
                        cur_size += 1
            present_sizes.append(cur_size)

        valid_count = 0
        for line in lines[30:]:
            numbers = helpers.parse_all_numbers(line)
            area = numbers[0] * numbers[1]
            present_size = sum(map(operator.mul, numbers[2:], present_sizes))

            if present_size < area:
                valid_count += 1
        return valid_count

    def solve_puzzle_two(self):
        return 'ALL DONE!'
