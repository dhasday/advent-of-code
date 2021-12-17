from aoc.common import helpers
from aoc.common.day_solver import DaySolver


class Day17Solver(DaySolver):
    year = 2021
    day = 17

    def solve_puzzles(self):
        bounds = Bounds(self.load_only_input_line())

        all_hits = []
        for x in range(bounds.max_x + 1):
            for y in range(bounds.min_y, -bounds.min_y):
                highest_y = self._process_shot(bounds, x, y)
                if highest_y is not None:
                    all_hits.append(highest_y)

        return max(all_hits), len(all_hits)

    def _process_shot(self, bounds, initial_x, initial_y):
        pos = 0, 0
        offset = initial_x, initial_y
        y_values = set()
        y_values.add(0)
        while pos[0] <= bounds.max_x and pos[1] >= bounds.min_y:
            pos = pos[0] + offset[0], pos[1] + offset[1]
            y_values.add(pos[1])
            if bounds.in_range(pos):
                return max(y_values)
            offset = max(offset[0] - 1, 0), offset[1] - 1

        return None


class Bounds(object):
    def __init__(self, line):
        self.min_x, self.max_x, self.min_y, self.max_y = [
            int(v) for v in helpers.ALL_NUMBERS_REGEX.findall(line)
        ]

    def in_range(self, pos):
        return self.min_x <= pos[0] <= self.max_x \
               and self.min_y <= pos[1] <= self.max_y
