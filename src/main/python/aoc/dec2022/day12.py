import math
import string
from collections import deque, defaultdict

from aoc.common.day_solver import DaySolver
from aoc.common.dijkstra_search import DijkstraSearch
from aoc.common.helpers import STANDARD_DIRECTIONS


class Day12Solver(DaySolver):
    year = 2022
    day = 12

    def solve_puzzles(self):
        lines = self.load_all_input_lines()

        start_pos = None
        start_options = []
        end_pos = None
        grid = []
        for r, line in enumerate(lines):
            row = []
            for c, v in enumerate(line):
                if v == 'S':
                    start_pos = r, c
                    v = 'a'
                if v == 'E':
                    end_pos = r, c
                    v = 'z'
                row.append(ord(v))
                if v == 'a':
                    start_options.append((r, c))
            grid.append(row)

        max_rows = len(grid)
        max_cols = len(grid[0])

        def find_adjacent_nodes(node):
            (cur_r, cur_c) = node
            cur_val = grid[cur_r][cur_c]

            adj = []
            for (dr, dc) in STANDARD_DIRECTIONS:
                next_r = cur_r + dr
                next_c = cur_c + dc

                if 0 <= next_r < max_rows \
                        and 0 <= next_c < max_cols \
                        and grid[next_r][next_c] >= cur_val - 1:
                    adj.append(((next_r, next_c), 1))

            return adj

        search = DijkstraSearch(find_adjacent_nodes)

        closed_set = search._execute_search(end_pos)

        part_1 = closed_set[start_pos].distance
        part_2 = min(closed_set[p].distance for p in start_options if p in closed_set)

        return part_1, part_2
