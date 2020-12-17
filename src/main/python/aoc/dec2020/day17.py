import re

from aoc.common.day_solver import DaySolver

INPUT_REGEX = re.compile(r'')
OFFSETS = [-1, 0, 1]


class Day17Solver(DaySolver):
    year = 2020
    day = 17

    def solve_puzzle_one(self):
        lines = self.load_all_input_lines()

        active_points = set()

        for y, line in enumerate(lines):
            for x, c in enumerate(line):
                if c == '#':
                    active_points.add((x, y, 0))

        for _ in range(6):
            active_points = self._step_3d(active_points)
        return len(active_points)

    def solve_puzzle_two(self):
        lines = self.load_all_input_lines()

        active_points = set()

        for y, line in enumerate(lines):
            for x, c in enumerate(line):
                if c == '#':
                    active_points.add((x, y, 0, 0))

        for _ in range(6):
            active_points = self._step_4d(active_points)

        return len(active_points)

    def _step_3d(self, active_points):
        min_point, max_point = self._find_bounds_3d(active_points)

        new_active_points = set()
        for x in range(min_point[0] - 1, max_point[0] + 2):
            for y in range(min_point[1] - 1, max_point[1] + 2):
                for z in range(min_point[2] - 1, max_point[2] + 2):
                    num_neighbors = self._num_neighbors_3d(active_points, x, y, z)

                    point = x, y, z
                    if (point in active_points and num_neighbors in [2, 3]) \
                            or (point not in active_points and num_neighbors == 3):
                        new_active_points.add(point)

        return new_active_points

    def _find_bounds_3d(self, points):
        min_x = min_y = min_z = max_x = max_y = max_z = 0

        for point in points:
            min_x = min(min_x, point[0])
            min_y = min(min_y, point[1])
            min_z = min(min_z, point[2])

            max_x = max(max_x, point[0])
            max_y = max(max_y, point[1])
            max_z = max(max_z, point[2])

        min_point = min_x, min_y, min_z
        max_point = max_x, max_y, max_z
        return min_point, max_point

    def _num_neighbors_3d(self, active_points, x, y, z):
        num_neighbors = 0
        for o_x in OFFSETS:
            for o_y in OFFSETS:
                for o_z in OFFSETS:
                    if o_x == 0 and o_y == 0 and o_z == 0:
                        continue
                    point = o_x + x, o_y + y, o_z + z
                    if point in active_points:
                        num_neighbors += 1

        return num_neighbors

    def _step_4d(self, active_points):
        min_point, max_point = self._find_bounds_4d(active_points)

        new_active_points = set()
        for x in range(min_point[0] - 1, max_point[0] + 2):
            for y in range(min_point[1] - 1, max_point[1] + 2):
                for z in range(min_point[2] - 1, max_point[2] + 2):
                    for w in range(min_point[3] - 1, max_point[3] + 2):
                        num_neighbors = self._num_neighbors_4d(active_points, x, y, z, w)

                        point = x, y, z, w
                        if (point in active_points and num_neighbors in [2, 3]) \
                                or (point not in active_points and num_neighbors == 3):
                            new_active_points.add(point)

        return new_active_points

    def _find_bounds_4d(self, points):
        min_x = min_y = min_z = min_w = max_x = max_y = max_z = max_w = 0

        for point in points:
            min_x = min(min_x, point[0])
            min_y = min(min_y, point[1])
            min_z = min(min_z, point[2])
            min_w = min(min_w, point[3])

            max_x = max(max_x, point[0])
            max_y = max(max_y, point[1])
            max_z = max(max_z, point[2])
            max_w = max(max_w, point[3])

        min_point = min_x, min_y, min_z, min_w
        max_point = max_x, max_y, max_z, max_w
        return min_point, max_point

    def _num_neighbors_4d(self, active_points, x, y, z, w):
        num_neighbors = 0
        for o_x in OFFSETS:
            for o_y in OFFSETS:
                for o_z in OFFSETS:
                    for o_w in OFFSETS:
                        if o_x == 0 and o_y == 0 and o_z == 0 and o_w == 0:
                            continue
                        point = o_x + x, o_y + y, o_z + z, o_w + w
                        if point in active_points:
                            num_neighbors += 1

        return num_neighbors
