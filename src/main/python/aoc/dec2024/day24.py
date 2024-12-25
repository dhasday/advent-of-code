from collections import deque, defaultdict

from aoc.common import helpers
from aoc.common.day_solver import DaySolver


class Day24Solver(DaySolver):
    year = 2024
    day = 24

    def solve_puzzle_one(self):
        lines = self.load_all_input_lines()

        split = lines.index('')

        state = dict()
        for line in lines[:split]:
            wire, value = line.split(': ')
            state[wire] = int(value)

        result = self._process_instructions(state, lines[split + 1:])
        return helpers.binary_to_decimal(result)

    def solve_puzzle_two(self):
        """
        The instructions compose the logic for an adder with some errors. Given this, we can look
        for mismatches between the expected operations

        First Bit:
        A ^ B -> output
        A & B -> carry

        General Case:
        A ^ B -> partial_1
        partial_1 ^ C' -> output
        A & B -> partial_2
        partial_1 & C' -> carry
        """
        lines = self.load_all_input_lines()

        instructions = []
        usages = defaultdict(list)
        for line in lines[lines.index('') + 1:]:
            left, op, right, _, out = line.split(' ')
            operation = (left[0] in 'xy', op, right[0] in 'xy', out)
            usages[left].append(op)
            usages[right].append(op)

            if out != 'z45' and left != 'x00':
                instructions.append(operation)

        for key in usages:
            usages[key] = sorted(usages[key])

        swapped = set()
        for left_is_input, op, right_is_input, out in instructions:
            match op:
                case 'XOR':
                    if not self._is_valid_xor(usages, left_is_input, right_is_input, out):
                        swapped.add(out)
                case 'AND':
                    if not self._is_valid_and(usages, left_is_input, right_is_input, out):
                        swapped.add(out)
                case 'OR':
                    if not self._is_valid_or(usages, left_is_input, right_is_input, out):
                        swapped.add(out)
        return ','.join(sorted(swapped))

    def _process_instructions(self, state, start_instructions):
        instructions = deque(start_instructions)
        while instructions:
            cur_inst = instructions.popleft()
            left, op, right, _, out = cur_inst.split(' ')
            if left not in state or right not in state:
                instructions.append(cur_inst)
            else:
                if op == 'AND':
                    result = state[left] & state[right]
                elif op == 'OR':
                    result = state[left] | state[right]
                elif op == 'XOR':
                    result = state[left] ^ state[right]
                else:
                    raise Exception('Unknown op {}'.format(op))

                state[out] = result

        return self._print_value(state, 'z')

    def _print_value(self, state, prefix):
        result = ''
        for key in reversed(sorted(state.keys())):
            if key[0] == prefix:
                result += str(state[key])
        return result

    def _is_valid_xor(self, usages, left_is_input, right_is_input, out):
        if left_is_input:
            if not right_is_input:
                return False  # Either both or neither should be inputs
            if out[0] == 'z' and out != 'z00':
                return False  # Can't go directly to output from input
            if out != 'z00' and usages[out] != ['AND', 'XOR']:
                return False  # Operations using output do not match expected
        elif out[0] != 'z':
            return False  # Output must by z if no inputs

        return True

    def _is_valid_and(self, usages, left_is_input, right_is_input, out):
        if left_is_input and not right_is_input:
            return False  # Either both or neither should be inputs
        if usages[out] != ['OR']:
            return False  # Operations using output do not match expected

        return True

    def _is_valid_or(self, usages, left_is_input, right_is_input, out):
        if left_is_input or right_is_input:
            return False  # Neither operand should be an input
        if usages[out] != ['AND', 'XOR']:
            return False  # Operations using output do not match expected

        return True
