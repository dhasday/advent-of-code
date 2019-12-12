import math
import re

from aoc.common.day_solver import DaySolver
from aoc.dec2019.common.intcode_processor import IntcodeProcessor
from aoc.dec2019.common.letter_reader import read_output

ALL_NUMBERS_REGEX = re.compile(r'-?\d+')


class Day12Solver(DaySolver):
    year = 2019
    day = 12

    def solve_puzzle_one(self):
        pos, vel = self._init_input()

        for i in range(1000):
            self._run_step(pos, vel)

        return self._total_energy(pos, vel)

    def solve_puzzle_two(self):
        pos, vel = self._init_input()

        seen = [set(), set(), set()]
        cycles = [None, None, None]
        remaining = 3

        i = 0
        while remaining:
            for j in range(3):
                if cycles[j] is None:
                    r = ','.join(str(v) for v in (pos[j::3] + vel[j::3]))
                    if r in seen[j]:
                        cycles[j] = i
                        remaining -= 1
                    else:
                        seen[j].add(r)

            self._run_step(pos, vel)
            i += 1

        return self._lcm(cycles)

    def _init_input(self):
        lines = self._load_all_input_lines()

        pos = list(int(v) for v in ALL_NUMBERS_REGEX.findall(''.join(lines)))
        vel = [0] * len(pos)
        return pos, vel

    def _run_step(self, pos, vel):
        for i in range(3):
            for j in range(i + 1, 4):
                for x in range(3):
                    idx_1 = i * 3 + x
                    idx_2 = j * 3 + x
                    if pos[idx_1] < pos[idx_2]:
                        vel[idx_1] += 1
                        vel[idx_2] -= 1
                    elif pos[idx_1] > pos[idx_2]:
                        vel[idx_1] -= 1
                        vel[idx_2] += 1

        for i in range(len(pos)):
            pos[i] += vel[i]

    def _total_energy(self, pos, vel):
        total = 0

        for i in range(4):
            pot = 0
            kin = 0
            for j in range(3):
                pot += abs(pos[i * 3 + j])
                kin += abs(vel[i * 3 + j])
            total += pot * kin

        return total

    def _lcm(self, values):
        lcm = values[0]
        for v in values[1:]:
            gcd = math.gcd(lcm, v)
            lcm = abs(lcm * v) // gcd

        return lcm
