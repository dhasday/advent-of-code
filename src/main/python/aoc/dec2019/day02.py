from aoc.common.day_solver import DaySolver
from aoc.dec2019.common.intcode_processor import IntcodeProcessor

SEQUENCE_START_VALUE = 0


class Day02Solver(DaySolver):
    year = 2019
    day = 2

    def solve_puzzle_one(self):
        line = self._load_only_input_line()

        processor = IntcodeProcessor(program_str=line)

        processor.program[1] = 12
        processor.program[2] = 2

        processor.run_until_completion()
        return processor.program[0]

    def solve_puzzle_two(self):
        line = self._load_only_input_line()

        processor = IntcodeProcessor(program_str=line)

        for i in range(0, 99):
            for j in range(0, 99):
                processor.reset()
                processor.program[1] = i
                processor.program[2] = j

                processor.run_until_completion()

                if processor.program[0] == 19690720:
                    return (i * 100) + j

        return None
