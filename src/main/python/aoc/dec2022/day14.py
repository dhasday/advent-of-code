from aoc.common.day_solver import DaySolver
from aoc.common.helpers import ALL_NUMBERS_REGEX


START_POS = (500, 0)


class Day14Solver(DaySolver):
    year = 2022
    day = 14

    grid = None
    max_y = None

    def setup(self):
        lines = self.load_all_input_lines()

        self.grid = set()
        self.max_y = 0
        for line in lines:
            values = [int(v) for v in ALL_NUMBERS_REGEX.findall(line)]
            for i in range(0, len(values) - 2, 2):
                x1, x2 = sorted([values[i], values[i+2]])
                y1, y2 = sorted([values[i+1], values[i+3]])
                for x in range(x1, x2 + 1):
                    for y in range(y1, y2 + 1):
                        self.grid.add((x, y))
                self.max_y = max(self.max_y, y2)

    def solve_puzzle_one(self):
        grid = self.grid.copy()

        for i in range(1000):
            next_pos = self._add_sand(grid, START_POS, self.max_y)
            if next_pos is None:
                return i

        return 'ERROR'

    def solve_puzzle_two(self):
        grid = self.grid.copy()

        for i in range(50000):
            next_pos = self._add_sand(grid, START_POS, self.max_y)
            if next_pos == START_POS:
                return i + 1

        return 'ERROR'

    def _add_sand(self, grid, start_pos, max_y):
        cur_pos = start_pos

        while True:
            # If we fell off the bottom, become the new bottom
            if cur_pos[1] > max_y:
                grid.add(cur_pos)
                return None

            down = cur_pos[0], cur_pos[1] + 1
            if down not in grid:
                cur_pos = down
                continue

            left = cur_pos[0] - 1, cur_pos[1] + 1
            if left not in grid:
                cur_pos = left
                continue

            right = cur_pos[0] + 1, cur_pos[1] + 1
            if right not in grid:
                cur_pos = right
                continue

            grid.add(cur_pos)
            return cur_pos
