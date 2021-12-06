from collections import Counter, defaultdict

from aoc.common.day_solver import DaySolver
from aoc.common.helpers import ALL_NUMBERS_REGEX


class Day06Solver(DaySolver):
    year = 2021
    day = 6

    def solve_puzzles(self):
        line = self.load_only_input_line()
        fish_count = Counter(int(v) for v in ALL_NUMBERS_REGEX.findall(line))

        for i in range(80):
            fish_count = self._advance_day(fish_count)
        part_1 = sum(fish_count.values())

        for i in range(256 - 80):
            fish_count = self._advance_day(fish_count)
        part_2 = sum(fish_count.values())

        return part_1, part_2

    def _advance_day(self, cur_fish_count):
        new_fish_count = defaultdict(lambda: 0)

        for fish, count in cur_fish_count.items():
            if fish == 0:
                new_fish_count[6] += count
                new_fish_count[8] += count
            else:
                new_fish_count[fish - 1] += count

        return new_fish_count
