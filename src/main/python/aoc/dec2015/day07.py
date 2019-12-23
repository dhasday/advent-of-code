import re

from aoc.common.day_solver import DaySolver

INPUT_REGEX = re.compile('')

ASSIGNMENT_PATTERN = re.compile('(NOT )?([a-z]+|[0-9]+) -> ([a-z]+)')
OPERATION_PATTERN = re.compile('([a-z]+|[0-9]+) (AND|OR|LSHIFT|RSHIFT) ([a-z]+|[0-9]+) -> ([a-z]+)')

OP_ASSIGN = 0
OP_ASSIGN_INVERSE = 1
OP_AND = 2
OP_OR = 3
OP_LSHIFT = 4
OP_RSHIFT = 5

OP_DICT = {
    'AND': OP_AND,
    'OR': OP_OR,
    'LSHIFT': OP_LSHIFT,
    'RSHIFT': OP_RSHIFT,
}


class Day07Solver(DaySolver):
    year = 2015
    day = 7

    class VariableState(object):
        def __init__(self, instruction, value=None):
            self.instruction = instruction
            self.value = value

        def process_value(self, registers):
            if self.value is None:
                self.value = self.instruction.perform_op(registers)
            return self.value

        def __str__(self):
            return str(self.value)

    class Instruction(object):
        input_one = None
        input_two = None
        output = None
        op = None

        def __init__(self, line):
            result = ASSIGNMENT_PATTERN.match(line)
            if result is not None:
                self.op = OP_ASSIGN_INVERSE if result.group(1) else OP_ASSIGN
                self.input_one = result.group(2)
                self.output = result.group(3)
            else:
                result = OPERATION_PATTERN.match(line)
                self.op = OP_DICT.get(result.group(2))
                self.input_one = result.group(1)
                self.input_two = result.group(3)
                self.output = result.group(4)

        def perform_op(self, registers):
            if self.op == OP_ASSIGN:
                value = self._get_value(registers, self.input_one)
                result = value
            elif self.op == OP_ASSIGN_INVERSE:
                value = self._get_value(registers, self.input_one)
                result = ~value  # TODO: Need to mod by max value?
            elif self.op == OP_AND:
                value_one = self._get_value(registers, self.input_one)
                value_two = self._get_value(registers, self.input_two)
                result = value_one & value_two
            elif self.op == OP_OR:
                value_one = self._get_value(registers, self.input_one)
                value_two = self._get_value(registers, self.input_two)
                result = value_one | value_two
            elif self.op == OP_LSHIFT:
                value_one = self._get_value(registers, self.input_one)
                value_two = self._get_value(registers, self.input_two)
                result = value_one << value_two
            elif self.op == OP_RSHIFT:
                value_one = self._get_value(registers, self.input_one)
                value_two = self._get_value(registers, self.input_two)
                result = value_one >> value_two
            else:
                raise Exception('Don\'t know this instruction')

            return self._clear_high_bits(result)

        def _get_value(self, registers, operand):
            value = operand if operand.isdigit() else registers[operand].process_value(registers)
            return self._clear_high_bits(value)

        def _clear_high_bits(self, value):
            return int(value) % 65536

    def solve_puzzles(self):
        lines = self.load_all_input_lines()

        registers = dict()
        for l in lines:
            instruction = self.Instruction(l)
            registers[instruction.output] = self.VariableState(instruction)

        ans_one = registers['a'].process_value(registers)

        for r in registers:
            registers[r].value = None

        registers['b'].value = ans_one
        ans_two = registers['a'].process_value(registers)

        return ans_one, ans_two
