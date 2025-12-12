import math

from aoc.common import helpers
from aoc.common.day_solver import DaySolver


class Day06Solver(DaySolver):
    year = 2025
    day = 6

    def solve_puzzle_one(self):
        lines = self.load_all_input_lines()

        numbers = []
        for line in lines[:-1]:
            numbers.append(helpers.parse_all_numbers(line))

        total = 0
        for idx, op in enumerate(lines[-1].replace(' ', '')):
            if op == '*':
                total += math.prod(n[idx] for n in numbers)
            elif op == '+':
                total += sum(n[idx] for n in numbers)
            else:
                raise Exception(f'Invalid operation: {op}')
        return total

    def solve_puzzle_two(self):
        # lines = self.load_all_input_lines(example=True)
        lines = self.load_all_input_lines()

        # Pad lines to ensure they are all the same length and that they end with a space
        max_length = max(len(line) for line in lines)
        for i in range(len(lines)):
            line_length = len(lines[i])
            if line_length < max_length:
                lines[i] += ' ' * (max_length - line_length)

        total = 0
        cur_total = 0
        cur_op = None
        for idx in range(max_length):
            char = lines[-1][idx]
            if char == '*':
                cur_total = 1
                cur_op = lambda v: cur_total * int(v)
            elif char == '+':
                cur_total = 0
                cur_op = lambda v: cur_total + int(v)

            cur_value = ''.join(line[idx] for line in lines[:-1] if line[idx] != ' ')
            if cur_value:
                cur_total = cur_op(cur_value)
            else:
                total += cur_total
                cur_total = 0

        return total
