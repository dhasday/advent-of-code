from collections import deque
from copy import deepcopy

from aoc.common.day_solver import DaySolver


class Day25Solver(DaySolver):
    year = 2021
    day = 25

    def solve_puzzle_one(self):
        lines = self.load_all_input_lines()

        grid = [[v for v in line] for line in lines]

        size_x = len(grid[0])
        size_y = len(grid)
        for i in range(1, 500):
            grid, n_moves_right = self._process_moves(grid, size_x, size_y)
            # grid, n_moves_down = self._process_move_down(grid, size_x, size_y)
            if n_moves_right == 0:
                return i

        return 'ERROR'

    def solve_puzzle_two(self):
        return 'ALL DONE!'

    def _process_moves(self, grid, size_x, size_y):
        num_moves = 0
        next_grid = [['.'] * size_x for _ in range(size_y)]
        for y in range(size_y):
            for x in range(size_x):
                val = grid[y][x]
                if val == '>':
                    cmp_idx_x = 0 if x == (size_x - 1) else x + 1
                    if grid[y][cmp_idx_x] == '.':
                        next_grid[y][cmp_idx_x] = val
                        num_moves += 1
                    else:
                        next_grid[y][x] = val
                elif val == 'v':
                    cmp_idx_y = 0 if y == (size_y - 1) else y + 1
                    if self._can_move_down(grid, size_x, x, cmp_idx_y):
                        next_grid[cmp_idx_y][x] = val
                        num_moves += 1
                    else:
                        next_grid[y][x] = val
        return next_grid, num_moves

    def _can_move_down(self, grid, size_x, x, y):
        if grid[y][x] == '.':
            cmp_idx_x = size_x - 1 if x == 0 else x - 1
            return grid[y][cmp_idx_x] != '>'
        elif grid[y][x] == '>':
            cmp_idx_x = 0 if x == (size_x - 1) else x + 1
            return grid[y][cmp_idx_x] == '.'

        return False
