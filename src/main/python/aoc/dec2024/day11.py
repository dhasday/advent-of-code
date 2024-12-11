from functools import cache

from aoc.common.day_solver import DaySolver


class Day11Solver(DaySolver):
    year = 2024
    day = 11

    def solve_puzzles(self):
        stones = self.load_only_input_line().split(' ')

        total_p1 = 0
        total_p2 = 0

        for stone in stones:
            stone = int(stone)
            total_p1 += self.process_stone(stone, 25)
            total_p2 += self.process_stone(stone, 75)

        return total_p1, total_p2

    @cache
    def process_stone(self, value, num_iters):
        if num_iters == 0:
            return 1

        if value == 0:
            return self.process_stone(1, num_iters - 1)

        value_length = len(str(value))
        div, rem = divmod(value_length, 2)
        if rem == 0:
            return (
                    self.process_stone(int(str(value)[:div]), num_iters - 1) +
                    self.process_stone(int(str(value)[div:]), num_iters - 1)
            )

        return self.process_stone(value * 2024, num_iters - 1)
