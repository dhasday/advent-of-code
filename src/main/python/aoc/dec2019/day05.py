from aoc.common.day_solver import DaySolver
from aoc.dec2019.common.intcode_processor import IntcodeProcessor


class Day05Solver(DaySolver):
    year = 2019
    day = 5

    def solve_puzzle_one(self):
        line = self._load_only_input_line()

        processor = IntcodeProcessor(program_str=line, input_value=1)
        processor.run_until_completion()
        return processor.last_output

    def solve_puzzle_two(self):
        line = self._load_only_input_line()

        processor = IntcodeProcessor(program_str=line, input_value=5)
        processor.run_until_completion()
        return processor.last_output
