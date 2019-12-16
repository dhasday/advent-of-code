import math
import re
from collections import deque
from itertools import islice, cycle

from aoc.common.day_solver import DaySolver
from aoc.common.dijkstra_search import DijkstraSearch
from aoc.dec2019.common.intcode_processor import IntcodeProcessor

ALL_NUMBERS_REGEX = re.compile(r'-?\d+')

BASE_PATTERN = [0, 1, 0, -1]


class Day16Solver(DaySolver):
    year = 2019
    day = 16

    def solve_puzzle_one(self):
        values = [int(c) for c in self._load_only_input_line()]

        for i in range(100):
            values = self._iterate_values(values)

        return ''.join(str(v) for v in values[:8])

    def solve_puzzle_two(self):
        values = [int(c) for c in self._load_only_input_line()] * 10000
        message_offset = int(''.join(str(v) for v in values[:7]))

        values = values[message_offset:]

        for i in range(100):
            values = self._iterate_sum_remaining(values)

        return ''.join(str(v) for v in values[:8])

    def _iterate_values(self, values):
        num_values = len(values)
        halfway = num_values // 2 + (num_values % 2)

        output = [0] * halfway
        for i in range(halfway):
            sequence = self._get_full_sequence(i)

            out_value = 0
            for j in range(num_values):
                out_value += values[j] * sequence[(j + 1) % len(sequence)]

            output[i] = abs(out_value) % 10

        output.extend(self._iterate_sum_remaining(values[halfway:]))

        return output

    def _iterate_sum_remaining(self, values):
        num_values = len(values)

        s = sum(values)
        output = []
        for i in range(num_values):
            output.append(abs(s) % 10)
            s -= values[i]
        return output

    def _get_full_sequence(self, idx):
        full_sequence = []
        for c in BASE_PATTERN:
            full_sequence.extend([c] * (idx + 1))
        return full_sequence
