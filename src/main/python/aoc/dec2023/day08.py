import re

from aoc.common import helpers
from aoc.common.day_solver import DaySolver


class Day08Solver(DaySolver):
    year = 2023
    day = 8

    sequence = None
    mapping = None

    def setup(self):
        lines = self.load_all_input_lines()

        self.sequence = lines[0]

        line_regex = re.compile(r'([A-Z0-9]{3}) = \(([A-Z0-9]{3}), ([A-Z0-9]{3})\)')
        self.mapping = {}
        for line in lines[2:]:
            match = line_regex.match(line)
            self.mapping[match.group(1)] = (match.group(2), match.group(3))

    def solve_puzzle_one(self):
        start = 'AAA'
        target = 'ZZZ'

        cur = start
        count = 0
        len_sequence = len(self.sequence)
        while cur != target:
            cur = self._get_next(cur, count % len_sequence)
            count += 1

        return count

    def solve_puzzle_two(self):
        starts = [key for key in self.mapping.keys() if key[2] == 'A']
        ends = [key for key in self.mapping.keys() if key[2] == 'Z']

        len_sequence = len(self.sequence)
        cycle_sizes = []
        for start in starts:
            # Determine the cycle time from start to first finish (initial offset)
            count = 0
            cur = start
            while cur not in ends:
                cur = self._get_next(cur, count % len_sequence)
                count += 1

            # Determine the cycle time from first finish to second finish (loop size)
            target = cur
            cur = self._get_next(cur, count % len_sequence)
            loop_count = count + 1
            while cur != target:
                cur = self._get_next(cur, loop_count % len_sequence)
                loop_count += 1

            # The data appears to match the cycle size for both the initial offset and loop size,
            # so assert that is the case to be able to just use LCM to get the answer, assuming
            # all cycles are the same and start at t=0
            assert(count == loop_count - count)

            cycle_sizes.append(count)

        return helpers.lcm(cycle_sizes)

    def _get_next(self, cur, idx):
        if self.sequence[idx] == 'L':
            return self.mapping[cur][0]
        else:
            return self.mapping[cur][1]
