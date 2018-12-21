import re
from collections import defaultdict

from aoc.common.day_solver import DaySolver

ALL_NUMBERS_REGEX = re.compile('-?\d+')


def _execute(func):
    def cmd(cur_registers, instruction):
        output = cur_registers[::]
        output[instruction[3]] = func(cur_registers, instruction[1], instruction[2])
        return output

    return cmd


class Day16Solver(DaySolver):
    year = 2018
    day = 16

    operations = [
        _execute(lambda r, a, b: r[a] + r[b]),                  # addr
        _execute(lambda r, a, b: r[a] + b),                     # addi
        _execute(lambda r, a, b: r[a] * r[b]),                  # mulr
        _execute(lambda r, a, b: r[a] * b),                     # muli
        _execute(lambda r, a, b: r[a] & r[b]),                  # banr
        _execute(lambda r, a, b: r[a] & b),                     # bani
        _execute(lambda r, a, b: r[a] | r[b]),                  # borr
        _execute(lambda r, a, b: r[a] | b),                     # bori
        _execute(lambda r, a, b: r[a]),                         # setr
        _execute(lambda r, a, b: a),                            # seti
        _execute(lambda r, a, b: 1 if a > r[b] else 0),         # gtir
        _execute(lambda r, a, b: 1 if r[a] > b else 0),         # gtri
        _execute(lambda r, a, b: 1 if r[a] > r[b] else 0),      # gtrr
        _execute(lambda r, a, b: 1 if a == r[b] else 0),        # eqir
        _execute(lambda r, a, b: 1 if r[a] == b else 0),        # eqri
        _execute(lambda r, a, b: 1 if r[a] == r[b] else 0),     # eqrr
    ]

    def solve_puzzles(self):
        part_one_input, part_two_input = self._load_input()

        ans_one, opcodes = self._solve_part_one(part_one_input)
        ans_two = self._solve_part_two(part_two_input, opcodes)

        return ans_one, ans_two

    def _load_input(self):
        filename = self._get_input_filename()

        samples, program = open(filename).read().strip().split('\n\n\n\n')
        samples = samples.split('\n')
        program = program.split('\n')

        part_one_input = []
        for i in range(0, len(samples), 4):
            start = map(int, ALL_NUMBERS_REGEX.findall(samples[i]))
            instruction = map(int, ALL_NUMBERS_REGEX.findall(samples[i + 1]))
            end = map(int, ALL_NUMBERS_REGEX.findall(samples[i + 2]))
            part_one_input.append([start, instruction, end])

        part_two_input = [map(int, ALL_NUMBERS_REGEX.findall(i)) for i in program]

        return part_one_input, part_two_input

    def _solve_part_one(self, samples):
        ans_one = 0
        opcodes = defaultdict(lambda: set())
        for s in samples:
            start_registers, instruction, end_registers = s

            matching_count = 0
            for m in self.operations:
                op_result = m(start_registers, instruction)
                if op_result == end_registers:
                    matching_count += 1
                    opcodes[instruction[0]].add(m)

            if matching_count >= 3:
                ans_one += 1

        return ans_one, opcodes

    def _solve_part_two(self, instructions, opcodes):
        opcode_map = {}
        while len(opcode_map) < 16:
            for code in opcodes:
                if code in opcode_map:
                    continue

                cur_codes = opcodes[code].difference(opcode_map.values())
                if len(cur_codes) == 1:
                    opcode_map[code] = cur_codes.pop()

        registers = [0, 0, 0, 0]
        for instruction in instructions:
            registers = opcode_map[instruction[0]](registers, instruction)

        return registers[0]
