import re

from aoc.common.day_solver import DaySolver
from aoc.dec2019.common.intcode_processor import IntcodeProcessor

ALL_NUMBERS_REGEX = re.compile(r'-?\d+')


class Day09Solver(DaySolver):
    year = 2019
    day = 9

    def solve_puzzle_one(self):
        line = self._load_only_input_line()

        processor = IntcodeProcessor(line, input_value=1)
        processor.run_until_completion()
        return processor.last_output

    def solve_puzzle_two(self):
        line = self._load_only_input_line()

        processor = IntcodeProcessor(line, input_value=2)
        processor.run_until_completion()
        return processor.last_output
