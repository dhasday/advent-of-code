import re
from collections import defaultdict

from aoc.common import helpers
from aoc.common.day_solver import DaySolver

INPUT_REGEX = re.compile(r'')


class Day15Solver(DaySolver):
    year = 2020
    day = 15

    def solve_puzzles(self):
        line = self.load_only_input_line()
        numbers = [int(n) for n in line.split(',')]

        ans_one = self._run_n_times(numbers, 2000)
        ans_two = self._run_n_times(numbers, 30000000)

        return ans_one, ans_two

    def _run_n_times(self, seed_numbers, num_times):
        last_said = {
            num: idx
            for idx, num in enumerate(seed_numbers, start=1)
        }

        cur_idx = len(seed_numbers) + 1
        last_val = seed_numbers[-1]

        while cur_idx <= num_times:
            if last_val in last_said:
                next_val = cur_idx - last_said[last_val] - 1
            else:
                next_val = 0

            last_said[last_val] = cur_idx - 1
            last_val = next_val
            cur_idx += 1

        return last_val
