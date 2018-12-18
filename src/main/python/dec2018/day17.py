import re
import sys
from collections import defaultdict

from enum import Enum

from common.day_solver import DaySolver

sys.setrecursionlimit(3000)
WHOLE_NUMBERS_REGEX = re.compile('-?\d+')


class State(Enum):
    SPRING = '+'
    CLAY = '#'
    FLOWING_WATER = '|'
    SETTLED_WATER = '~'


class Day17Solver(DaySolver):
    year = 2018
    day = 17

    class Grid(object):
        grid = defaultdict()

        def get_value(self, pos):
            return self.grid.get(pos)

        def set_value(self, pos, value):
            self.grid[pos] = value

        def is_above(self, pos, value):
            below_pos = (pos[0], pos[1] + 1)
            return self.grid.get(below_pos) == value

        def visualize(self):
            min_x, max_x, min_y, max_y = self._find_bounds()
            size_x = max_x - min_x + 1
            size_y = max_y - min_y + 1
            rows = [' ' * size_x for _ in range(size_y)]

            for pos in self.grid:
                x_offset = pos[0] - min_x

                row = rows[pos[1]]
                rows[pos[1]] = row[:x_offset] + self.get_value(pos).value + row[x_offset + 1:]

            for row in rows:
                print row
            print

        def _find_bounds(self):
            min_x, min_y = max_x, max_y = None, None
            for (x, y) in self.grid:
                if min_x is None or x < min_x:
                    min_x = x
                if max_x is None or x > max_x:
                    max_x = x
                if min_y is None or y < min_y:
                    min_y = y
                if min_y is None or y > max_y:
                    max_y = y

            return min_x, max_x, min_y, max_y

    def solve_puzzles(self):
        grid, max_y = self._load_input()

        spring_pos = (500, 0)
        grid.set_value(spring_pos, State.SPRING)

        self._flow_water(grid, spring_pos, max_y)
        # grid.visualize()

        clay_depth_values = set(p[1] for p in grid.grid if grid.get_value(p) == State.CLAY)
        min_clay, max_clay = min(clay_depth_values), max(clay_depth_values)

        count_all_water = 0
        count_settled_water = 0
        for p in grid.grid:
            if min_clay <= p[1] <= max_clay:
                value = grid.get_value(p)
                if value == State.SETTLED_WATER:
                    count_all_water += 1
                    count_settled_water += 1
                elif value in [State.SPRING, State.FLOWING_WATER]:
                    count_all_water += 1

        return count_all_water, count_settled_water

    def _load_input(self, filename=None):
        grid = self.Grid()

        max_y = 0
        for line in self._load_all_input_lines(filename=filename):
            points = map(int, WHOLE_NUMBERS_REGEX.findall(line))

            if line[0] == 'x':
                x_range = range(points[0], points[0] + 1)
                y_range = range(points[1], points[2] + 1)
            elif line[0] == 'y':
                x_range = range(points[1], points[2] + 1)
                y_range = range(points[0], points[0] + 1)
            else:
                raise Exception('Something went wrong - ' + line)

            for x in x_range:
                for y in y_range:
                    if y > max_y:
                        max_y = y
                    grid.set_value((x, y), State.CLAY)

        return grid, max_y

    def _flow_water(self, grid, cur_pos, max_y):
        if cur_pos[1] >= max_y:
            return

        down_pos = cur_pos[0], cur_pos[1] + 1
        if grid.get_value(down_pos) is None:
            grid.set_value(down_pos, State.FLOWING_WATER)
            self._flow_water(grid, down_pos, max_y)

        left_pos = cur_pos[0] - 1, cur_pos[1]
        if grid.get_value(down_pos) in [State.CLAY, State.SETTLED_WATER] and grid.get_value(left_pos) is None:
            grid.set_value(left_pos, State.FLOWING_WATER)
            self._flow_water(grid, left_pos, max_y)

        right_pos = cur_pos[0] + 1, cur_pos[1]
        if grid.get_value(down_pos) in [State.CLAY, State.SETTLED_WATER] and grid.get_value(right_pos) is None:
            grid.set_value(right_pos, State.FLOWING_WATER)
            self._flow_water(grid, right_pos, max_y)

        wall_left, wall_right = self._find_walls(grid, cur_pos)
        if wall_left and wall_right:
            self._fill_level(grid, wall_left, wall_right)

    def _find_walls(self, grid, cur_pos):
        return self._find_wall(grid, cur_pos, -1), self._find_wall(grid, cur_pos, 1)

    def _find_wall(self, grid, start_pos, offset):
        cur_pos = start_pos
        cur_value = grid.get_value(cur_pos)

        while cur_value is not None and cur_value != State.CLAY:
            cur_pos = cur_pos[0] + offset, cur_pos[1]
            cur_value = grid.get_value(cur_pos)

        return cur_pos if grid.get_value(cur_pos) == State.CLAY else None

    def _fill_level(self, grid, wall_left, wall_right):
        for x in range(wall_left[0] + 1, wall_right[0]):
            for y in range(wall_left[1], wall_right[1] + 1):
                pos = x, y
                grid.set_value(pos, State.SETTLED_WATER)
