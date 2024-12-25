from collections import defaultdict

from aoc.common import helpers
from aoc.common.day_solver import DaySolver


class Day10Solver(DaySolver):
    year = 2024
    day = 10

    def solve_puzzles(self):
        lines = self.load_all_input_lines()

        height_to_pos = defaultdict(set)

        for y, line in enumerate(lines):
            for x, val in enumerate(line):
                height_to_pos[int(val)].add((x, y))

        available = [(v, v) for v in height_to_pos[0]]
        for i in range(1, 10):
            if not available:
                break

            next_available = []
            for start_pos, last_pos in available:
                for offset in helpers.STANDARD_DIRECTIONS:
                    next_pos = last_pos[0] + offset[0], last_pos[1] + offset[1]
                    if next_pos in height_to_pos[i]:
                        next_available.append((start_pos, next_pos))
            available = next_available

        return len(set(available)), len(available)
