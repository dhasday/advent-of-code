import math
import re

from aoc.common.day_solver import DaySolver


INPUT_REGEX = re.compile('([a-z]{4}) (\d+) (\d+) (\d+)')

INSTRUCTION_POINTER = 3


def _execute(func):
    def cmd(cur_registers, instruction):
        output = cur_registers[::]
        output[instruction[3]] = func(cur_registers, instruction[1], instruction[2])
        return output

    return cmd


operations = {
    'addr': _execute(lambda r, a, b: r[a] + r[b]),
    'addi': _execute(lambda r, a, b: r[a] + b),
    'mulr': _execute(lambda r, a, b: r[a] * r[b]),
    'muli': _execute(lambda r, a, b: r[a] * b),
    'banr': _execute(lambda r, a, b: r[a] & r[b]),
    'bani': _execute(lambda r, a, b: r[a] & b),
    'borr': _execute(lambda r, a, b: r[a] | r[b]),
    'bori': _execute(lambda r, a, b: r[a] | b),
    'setr': _execute(lambda r, a, b: r[a]),
    'seti': _execute(lambda r, a, b: a),
    'gtir': _execute(lambda r, a, b: 1 if a > r[b] else 0),
    'gtri': _execute(lambda r, a, b: 1 if r[a] > b else 0),
    'gtrr': _execute(lambda r, a, b: 1 if r[a] > r[b] else 0),
    'eqir': _execute(lambda r, a, b: 1 if a == r[b] else 0),
    'eqri': _execute(lambda r, a, b: 1 if r[a] == b else 0),
    'eqrr': _execute(lambda r, a, b: 1 if r[a] == r[b] else 0),
}


class Day19Solver(DaySolver):
    year = 2018
    day = 19

    # Analyzing the instructions reduced it to this:
    #
    # Initialize
    #   if R[0] == 0
    #       R[2] = 919
    #   if R[0] == 1
    #       R[2] = 10551319
    #
    # Do the operations (which is summing all the factors of the value in R[2])
    #   R[0] = 0
    #   R[4] = 1
    #   while R[4] <= R[2]:             # for 1..value
    #       R[5] = 1
    #       while R[5] <= R[2]:         # for 1..value
    #           if R[4] * R[5] == R[2]  # if factor
    #               R[0] += R[4]        #   add first factor
    #           R[5] += 1
    #       R[4] += 1

    def solve_puzzles(self):
        # return self._solve_puzzles_by_instructions()
        return self._solve_puzzles_by_simplification()

    def _solve_puzzles_by_simplification(self):
        part_one_val = 919
        part_two_val = 10551319

        ans_one = self._sum_of_factors(part_one_val)
        ans_two = self._sum_of_factors(part_two_val)

        return ans_one, ans_two

    def _sum_of_factors(self, value):
        factors = set()

        limit = int(math.sqrt(value))
        for i in range(1, limit):
            j, m = divmod(value, i)
            if m == 0:
                factors.add(i)
                factors.add(j)

        return sum(factors)

    def _solve_puzzles_by_instructions(self):
        instructions = self._load_input()

        # Part One
        registers = [0] * 6
        registers, ctr = self._run_until_halt(instructions, registers)
        ans_one = registers[0]

        # Part Two
        registers = [0] * 6
        registers[0] = 1
        registers = self._run_until_halt(instructions, registers)
        ans_two = registers[0]

        return ans_one, ans_two

    def _run_until_halt(self, instructions, start_registers):
        registers = start_registers
        cur_instruction = 0
        ctr = 0
        while 0 <= cur_instruction < len(instructions):
            instr = instructions[cur_instruction]

            registers[INSTRUCTION_POINTER] = cur_instruction
            registers = operations[instr[0]](registers, instr)

            cur_instruction = registers[INSTRUCTION_POINTER] + 1
            ctr += 1
        return registers, ctr

    def _load_input(self):
        instructions = []

        for line in self._load_all_input_lines():
            parsed = INPUT_REGEX.match(line)

            instruction = [
                parsed.group(1),
                int(parsed.group(2)),
                int(parsed.group(3)),
                int(parsed.group(4)),
            ]
            instructions.append(instruction)

        return instructions
