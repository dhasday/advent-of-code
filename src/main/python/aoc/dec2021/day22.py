from collections import defaultdict

from aoc.common.day_solver import DaySolver
from aoc.common.helpers import ALL_NUMBERS_REGEX


class Day22Solver(DaySolver):
    year = 2021
    day = 22

    def solve_puzzles(self):
        lines = self.load_all_input_lines()

        instructions = [self._parse_line(line) for line in lines]

        cubes = defaultdict(int)
        for toggle_on, current_dim in instructions:
            updated_cubes = defaultdict(int)
            if toggle_on:
                updated_cubes[current_dim] += 1

            for dim, count in cubes.items():
                intersection = self._get_intersection(current_dim, dim)
                if intersection is not None:
                    updated_cubes[intersection] -= count

            for dim, count in updated_cubes.items():
                cubes[dim] += count

        boot_total = 0
        total = 0
        boot_dim = CubeDimensions(-50, 50, -50, 50, -50, 50)
        for dim, count in cubes.items():
            total += dim.area() * count

            boot_intersection = self._get_intersection(boot_dim, dim)
            if boot_intersection:
                boot_total += boot_intersection.area() * count

        return boot_total, total

    def _parse_line(self, line):
        toggle_on = 'on' == line[0:2]
        nums = [int(v) for v in ALL_NUMBERS_REGEX.findall(line)]

        return (
            toggle_on,
            CubeDimensions(*nums)
        )

    def _get_intersection(self, dim_1, dim_2):
        if dim_1.min_x > dim_2.max_x or dim_1.max_x < dim_2.min_x:
            return None
        if dim_1.min_y > dim_2.max_y or dim_1.max_y < dim_2.min_y:
            return None
        if dim_1.min_z > dim_2.max_z or dim_1.max_z < dim_2.min_z:
            return None

        return CubeDimensions(
            max(dim_1.min_x, dim_2.min_x),
            min(dim_1.max_x, dim_2.max_x),
            max(dim_1.min_y, dim_2.min_y),
            min(dim_1.max_y, dim_2.max_y),
            max(dim_1.min_z, dim_2.min_z),
            min(dim_1.max_z, dim_2.max_z),
        )


class CubeDimensions(object):
    def __init__(self, min_x, max_x, min_y, max_y, min_z, max_z):
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y
        self.min_z = min_z
        self.max_z = max_z

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return hash(self) == hash(other)
        return False

    def __hash__(self):
        return hash((
            self.min_x,
            self.max_x,
            self.min_y,
            self.max_y,
            self.min_z,
            self.max_z,
        ))

    def area(self):
        return (self.max_x - self.min_x + 1) * (self.max_y - self.min_y + 1) * (self.max_z - self.min_z + 1)
