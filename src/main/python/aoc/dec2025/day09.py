from itertools import combinations, pairwise

from aoc.common import helpers
from aoc.common.day_solver import DaySolver


class Day09Solver(DaySolver):
    year = 2025
    day = 9

    def solve_puzzles(self):
        lines = self.load_all_input_lines()

        points = list()
        for line in lines:
            point = helpers.parse_all_numbers(line)
            points.append(tuple(point))

        max_area = 0
        max_in_region = 0
        for p1, p2 in combinations(points, 2):
            area = (abs(p1[0] - p2[0]) + 1) * (abs(p1[1] - p2[1]) + 1)
            max_area = max(area, max_area)
            if self._is_in_region(points, p1, p2):
                max_in_region = max(max_in_region, area)

        return max_area, max_in_region

    def _is_in_region(self, points, p1, p2):
        x_min, x_max = sorted([p1[0], p2[0]])
        y_min, y_max = sorted([p1[1], p2[1]])

        for (x1, y1), (x2, y2) in pairwise(points):
            if y1 == y2:
                if y_min < y1 < y_max and self._crosses_axis(x_min, x_max, x1, x2):
                    return False
            elif x1 == x2:
                if x_min < x1 < x_max and self._crosses_axis(y_min, y_max, y1, y2):
                    return False
            else:
                raise Exception(f"Invalid coordinate pair! {p1} and {p2}")

        return True

    def _crosses_axis(self, min_val, max_val, v1, v2):
        lower, higher = sorted([v1, v2])
        return lower <= min_val < higher or lower < max_val <= higher
