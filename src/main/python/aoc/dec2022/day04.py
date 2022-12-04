from aoc.common.day_solver import DaySolver
from aoc.common.helpers import ALL_DIGITS_REGEX


class Day04Solver(DaySolver):
    year = 2022
    day = 4

    def solve_puzzles(self):
        lines = self.load_all_input_lines()

        p1_count = 0
        p2_count = 0
        for line in lines:
            one_low, one_high, two_low, two_high = [int(v) for v in ALL_DIGITS_REGEX.findall(line)]

            if one_low == two_low:
                p1_count += 1
                p2_count += 1
            elif one_low < two_low:
                if one_high >= two_high:
                    p1_count += 1
                if one_high >= two_low:
                    p2_count += 1
            else:
                if two_high >= one_high:
                    p1_count += 1
                if two_high >= one_low:
                    p2_count += 1

        return p1_count, p2_count


Day04Solver().print_results()
