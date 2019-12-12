import math
import re

from aoc.common.day_solver import DaySolver
from aoc.dec2019.common.intcode_processor import IntcodeProcessor
from aoc.dec2019.common.letter_reader import read_output

ALL_NUMBERS_REGEX = re.compile(r'-?\d+')


class Day12Solver(DaySolver):
    year = 2019
    day = 12

    class Moon:
        def __init__(self, line):
            self.position = [int(v) for v in ALL_NUMBERS_REGEX.findall(line)]
            self.velocity = [0, 0, 0]

        def gravitate(self, moon):
            self._gravitate(moon, 0)
            self._gravitate(moon, 1)
            self._gravitate(moon, 2)

        def _gravitate(self, moon, idx):
            if self.position[idx] < moon.position[idx]:
                self.velocity[idx] += 1
                moon.velocity[idx] -= 1
            elif self.position[idx] > moon.position[idx]:
                self.velocity[idx] -= 1
                moon.velocity[idx] += 1

        def move(self):
            self.position[0] += self.velocity[0]
            self.position[1] += self.velocity[1]
            self.position[2] += self.velocity[2]

        def format_pair(self, idx):
            return '{},{}'.format(self.position[idx], self.velocity[idx])

        @property
        def total_energy(self):
            pot = sum(abs(p) for p in self.position)
            kin = sum(abs(v) for v in self.velocity)
            return pot * kin

    def solve_puzzle_one(self):
        lines = self._load_all_input_lines()
        moons = list(self.Moon(line) for line in lines)

        for i in range(1000):
            self._run_step(moons)

        return sum(m.total_energy for m in moons)

    def solve_puzzle_two(self):
        lines = self._load_all_input_lines()
        moons = list(self.Moon(line) for line in lines)

        targets = [' '.join(m.format_pair(i) for m in moons) for i in range(3)]
        cycles = [None, None, None]

        ctr = 0
        while not all(cycles) or ctr < 3000:
            self._run_step(moons)
            ctr += 1

            curs = ['', '', '']
            for m in moons:
                curs[0] += m.format_pair(0) + ' '
                curs[1] += m.format_pair(1) + ' '
                curs[2] += m.format_pair(2) + ' '

            if cycles[0] is None and targets[0] == curs[0][:-1]:
                cycles[0] = ctr
            if cycles[1] is None and targets[1] == curs[1][:-1]:
                cycles[1] = ctr
            if cycles[2] is None and targets[2] == curs[2][:-1]:
                cycles[2] = ctr

        return self._lcm(cycles)

    def _run_step(self, moons):
        num = len(moons)

        for i in range(num - 1):
            for j in range(i + 1, num):
                moons[i].gravitate(moons[j])

        for m in moons:
            m.move()

    def _lcm(self, values):
        lcm = values[0]
        for v in values[1:]:
            gcd = math.gcd(lcm, v)
            lcm = abs(lcm * v) // gcd

        return lcm
