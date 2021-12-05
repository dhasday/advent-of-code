import math
from collections import defaultdict

from aoc.common.day_solver import DaySolver
from aoc.common.helpers import ALL_NUMBERS_REGEX


class Day05Solver(DaySolver):
    year = 2021
    day = 5

    def solve_puzzles(self):
        lines = self.load_all_input_lines()

        flat_points = defaultdict(lambda: 0)
        diag_points = defaultdict(lambda: 0)
        for line in lines:
            values = [int(v) for v in ALL_NUMBERS_REGEX.findall(line)]
            pos_1 = values[0], values[1]
            pos_2 = values[2], values[3]

            if pos_1[0] == pos_2[0] or pos_1[1] == pos_2[1]:
                self._add_line(flat_points, pos_1, pos_2)
            else:
                self._add_line(diag_points, pos_1, pos_2)

        for pos, val in flat_points.items():
            diag_points[pos] += val

        return self._count_points(flat_points), self._count_points(diag_points)

    def _add_line(self, points, start, end):
        delta_x = end[0] - start[0]
        delta_y = end[1] - start[1]

        if delta_x == 0:
            delta_y //= abs(delta_y)
        elif delta_y == 0:
            delta_x //= abs(delta_x)
        else:
            lcm = math.lcm(delta_x, delta_y)
            delta_x //= lcm
            delta_y //= lcm

        cur_pos = start
        points[cur_pos] += 1
        while cur_pos != end:
            cur_pos = cur_pos[0] + delta_x, cur_pos[1] + delta_y
            points[cur_pos] += 1

    def _count_points(self, covered_points):
        return sum(1 for v in covered_points.values() if v > 1)
