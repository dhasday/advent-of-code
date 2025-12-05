from aoc.common.day_solver import DaySolver
from aoc.common.helpers import merge_ranges_d2


class Day05Solver(DaySolver):
    year = 2025
    day = 5

    def solve_puzzles(self):
        lines = self.load_all_input_lines()

        split_point = lines.index('')

        fresh_ranges = set()
        for line in lines[:split_point]:
            fresh_ranges.add(tuple(int(v) for v in line.split('-')))
        fresh_ranges = merge_ranges_d2(fresh_ranges)

        answer_one = 0
        for line in lines[split_point + 1:]:
            value = int(line)
            if next((1 for l, h in fresh_ranges if l <= value <= h), 0):
                answer_one += 1

        answer_two = sum(high - low + 1 for low, high in fresh_ranges)
        return answer_one, answer_two
