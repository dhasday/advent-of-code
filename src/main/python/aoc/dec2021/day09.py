from functools import reduce

from aoc.common.day_solver import DaySolver
from aoc.common.helpers import STANDARD_DIRECTIONS


class Day09Solver(DaySolver):
    year = 2021
    day = 9

    def solve_puzzles(self):
        lines = self.load_all_input_lines()

        grid = {}
        for y, line in enumerate(lines):
            for x, val in enumerate(line):
                grid[x, y] = int(val)

        part_1 = 0
        basins = set()
        for pos, val in grid.items():
            if self._is_local_minimum(grid, pos, val):
                basins.add(pos)
                part_1 += val + 1

        basin_sizes = []
        for basin in basins:
            basin_sizes.append(self._calculate_basin_size(grid, basin))

        part_2 = reduce(lambda b1, b2: b1 * b2, sorted(basin_sizes, reverse=True)[:3])

        return part_1, part_2

    def _is_local_minimum(self, grid, pos, val):
        for dx, dy in STANDARD_DIRECTIONS:
            adj = grid.get((pos[0] + dx, pos[1] + dy))
            if adj is not None and adj <= val:
                return False
        return True

    def _calculate_basin_size(self, grid, local_min):
        to_visit = {local_min}

        basin = set()
        while len(to_visit):
            cur_node = to_visit.pop()
            basin.add(cur_node)

            for dx, dy in STANDARD_DIRECTIONS:
                adj_pos = cur_node[0] + dx, cur_node[1] + dy
                if adj_pos not in basin:
                    adj_val = grid.get(adj_pos)
                    if adj_val is not None and adj_val < 9:
                        to_visit.add(adj_pos)

        return len(basin)
