import re

from aoc.common.day_solver import DaySolver

NUMBERS_REGEX = re.compile(r'(?=([0-9]|one|two|three|four|five|six|seven|eight|nine))')

VALUE_MAP = {
    '0': 0,
    '1': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
}


class Day01Solver(DaySolver):
    year = 2023
    day = 1

    def solve_puzzles(self):
        lines = self.load_all_input_lines()

        p1_total = 0
        p2_total = 0

        for line in lines:
            result = [r.group(1) for r in NUMBERS_REGEX.finditer(line)]

            p1_first = None
            p1_last = None
            for r in result:
                if len(r) == 1:
                    if p1_first is None:
                        p1_first = VALUE_MAP[r]
                    p1_last = VALUE_MAP[r]

            p2_first = VALUE_MAP[result[0]]
            p2_last = VALUE_MAP[result[-1]]

            p1_total += (p1_first * 10) + p1_last
            p2_total += (p2_first * 10) + p2_last

        return p1_total, p2_total
