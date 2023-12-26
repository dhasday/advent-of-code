import dataclasses
from functools import cache
from itertools import combinations

import z3

from aoc.common import helpers
from aoc.common.day_solver import DaySolver


@dataclasses.dataclass
class Hailstone:
    pos: tuple[int, int, int]
    vel: tuple[int, int, int]

    @cache
    def get_abc_2d(self):
        pos_2 = self.pos[0] + self.vel[0] * 5, self.pos[1] + self.vel[1] * 5

        a = pos_2[1] - self.pos[1]
        b = self.pos[0] - pos_2[0]
        c = a * self.pos[0] + b * self.pos[1]

        return a, b, c

    def __hash__(self):
        return hash(tuple([*self.pos, *self.vel]))


class Day24Solver(DaySolver):
    year = 2023
    day = 24

    hailstones = None

    def setup(self):
        lines = self.load_all_input_lines()

        self.hailstones = []
        for line in lines:
            numbers = [int(v) for v in helpers.ALL_NUMBERS_REGEX.findall(line)]
            self.hailstones.append(Hailstone(numbers[0:3], numbers[3:]))

    def solve_puzzle_one(self):
        min_value = 200000000000000
        max_value = 400000000000000

        def value_in_range(value):
            return min_value <= value <= max_value

        count = 0
        for h1, h2 in combinations(self.hailstones, 2):
            h1_a, h1_b, h1_c = h1.get_abc_2d()
            h2_a, h2_b, h2_c = h2.get_abc_2d()

            det = (h1_a * h2_b) - (h2_a * h1_b)
            if det == 0:
                continue

            x = ((h2_b * h1_c) - (h1_b * h2_c)) / det
            y = ((h1_a * h2_c) - (h2_a * h1_c)) / det

            t1 = (x - h1.pos[0]) / h1.vel[0]
            t2 = (x - h2.pos[0]) / h2.vel[0]
            t = min(t1, t2)

            if t >= 0 and value_in_range(x) and value_in_range(y):
                count += 1

        return count

    def solve_puzzle_two(self):
        px, py, pz, vx, vy, vz = z3.Ints("px py pz vx vy vz")
        times = [z3.Int("t" + str(i)) for i in range(len(self.hailstones))]

        s = z3.Solver()
        for i, hailstone in enumerate(self.hailstones):
            s.add(px + vx * times[i] == hailstone.pos[0] + hailstone.vel[0] * times[i])
            s.add(py + vy * times[i] == hailstone.pos[1] + hailstone.vel[1] * times[i])
            s.add(pz + vz * times[i] == hailstone.pos[2] + hailstone.vel[2] * times[i])
        s.check()
        ans = s.model().evaluate(px + py + pz)

        return ans.as_long()
