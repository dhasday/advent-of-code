from aoc.common.day_solver import DaySolver
from aoc.common.helpers import STANDARD_DIRECTIONAL_OFFSETS


class Day11Solver(DaySolver):
    year = 2021
    day = 11

    def solve_puzzles(self):
        grid = self._load_input()

        part_1 = 0
        for _ in range(100):
            grid, new_flashes = self._count_flashes(grid)
            part_1 += new_flashes

        for i in range(101, 500):
            grid, new_flashes = self._count_flashes(grid)
            if len(grid) == new_flashes:
                return part_1, i

        return part_1, 'ERROR'

    def _load_input(self, filename=None):
        lines = self.load_all_input_lines(filename)
        size_x = len(lines[0])
        size_y = len(lines)

        grid = {}
        for y in range(size_y):
            line = lines[y]
            for x in range(size_x):
                grid[x, y] = int(line[x])
        return grid

    def _count_flashes(self, grid):
        to_flash = set()
        for pos in grid.keys():
            grid[pos] += 1
            if grid[pos] > 9:
                to_flash.add(pos)

        seen = set()
        while to_flash:
            cur_pos = to_flash.pop()
            seen.add(cur_pos)
            grid[cur_pos] = 0

            for dx, dy in STANDARD_DIRECTIONAL_OFFSETS:
                adj_pos = cur_pos[0] + dx, cur_pos[1] + dy
                if adj_pos not in seen and adj_pos in grid:
                    grid[adj_pos] += 1
                    if grid[adj_pos] > 9:
                        to_flash.add(adj_pos)

        return grid, len(seen)
