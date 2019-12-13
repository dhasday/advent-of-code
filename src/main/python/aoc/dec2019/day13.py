import math
import re

from aoc.common.day_solver import DaySolver
from aoc.dec2019.common.intcode_processor import IntcodeProcessor
from aoc.dec2019.common.letter_reader import read_output

ALL_NUMBERS_REGEX = re.compile(r'-?\d+')


class Day13Solver(DaySolver):
    year = 2019
    day = 13

    def solve_puzzle_one(self):
        line = self._load_only_input_line()
        processor = IntcodeProcessor(program_str=line)

        num_blocks = 0
        while processor.last_opcode != 99:
            processor.get_next_output()
            processor.get_next_output()
            v = processor.get_next_output()

            if v == 2:
                num_blocks += 1

        return num_blocks

    def solve_puzzle_two(self):
        def determine_input():
            if ball[0] < paddle[0]:
                return -1
            elif ball[0] == paddle[0]:
                return 0
            else:
                return 1

        line = self._load_only_input_line()
        processor = IntcodeProcessor(program_str=line, input_func=determine_input)
        processor.program[0] = 2

        board = {}
        ball = (0, 0)
        paddle = (0, 0)
        score = 0
        while processor.last_opcode != 99:
            x = processor.get_next_output()
            y = processor.get_next_output()
            v = processor.get_next_output()

            point = x, y

            if point == (-1, 0):
                score = v
            else:
                board[point] = v

            if v == 3:
                paddle = point
            if v == 4:
                ball = point

        return score
