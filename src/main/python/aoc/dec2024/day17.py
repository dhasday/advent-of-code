from aoc.common import helpers
from aoc.common.day_solver import DaySolver


class ThreeBitComputer:
    def __init__(self, reg_a, reg_b, reg_c, instructions):
        self.orig_reg_a = reg_a
        self.reg_a = reg_a
        self.reg_b = reg_b
        self.reg_c = reg_c
        self.instructions = instructions
        self.ins_ptr = 0

    def reset(self, reg_a=None):
        self.reg_a = reg_a if reg_a is not None else self.orig_reg_a
        self.reg_b = 0
        self.reg_c = 0
        self.ins_ptr = 0

    def run(self):
        output = []
        while self.ins_ptr < len(self.instructions):
            out = self.process_instruction()
            if out is not None:
                output.append(out)
        return output

    def run_until_output(self):
        while self.ins_ptr < len(self.instructions):
            out = self.process_instruction()
            if out is not None:
                return out
        return None

    def run_for_output(self, target=None):
        if target is None:
            target = []

        idx = 0
        while idx < len(target):
            next_val = self.run_until_output()
            if next_val != target[idx]:
                return False
            idx += 1
        return True

    def process_instruction(self):
        opcode = self.instructions[self.ins_ptr]

        match opcode:
            case 0:
                return self.adv()
            case 1:
                return self.bxl()
            case 2:
                return self.bst()
            case 3:
                return self.jnz()
            case 4:
                return self.bxc()
            case 5:
                return self.out()
            case 6:
                return self.bdv()
            case 7:
                return self.cdv()

        raise Exception(f'Invalid opcode: {opcode}')

    def adv(self):
        self.reg_a = int(self.reg_a // (2 ** self._get_combo_operand_value()))
        self.ins_ptr += 2

    def bxl(self):
        self.reg_b = self.reg_b ^ self._get_literal_operand()
        self.ins_ptr += 2

    def bst(self):
        self.reg_b = self._get_combo_operand_value() % 8
        self.ins_ptr += 2

    def jnz(self):
        if self.reg_a == 0:
            self.ins_ptr += 2
        else:
            self.ins_ptr = self._get_literal_operand()

    def bxc(self):
        self.reg_b = self.reg_b ^ self.reg_c
        self.ins_ptr += 2

    def out(self):
        result = int(self._get_combo_operand_value() % 8)
        self.ins_ptr += 2
        return result

    def bdv(self):
        self.reg_b = int(self.reg_a // (2 ** self._get_combo_operand_value()))
        self.ins_ptr += 2

    def cdv(self):
        self.reg_c = int(self.reg_a // (2 ** self._get_combo_operand_value()))
        self.ins_ptr += 2

    def _get_literal_operand(self):
        return self.instructions[self.ins_ptr + 1]

    def _get_combo_operand_value(self):
        val = self._get_literal_operand()

        match val:
            case 0 | 1 | 2 | 3:
                return val
            case 4:
                return self.reg_a
            case 5:
                return self.reg_b
            case 6:
                return self.reg_c

        raise Exception(f"Invalid operand: {val}")


class Day17Solver(DaySolver):
    year = 2024
    day = 17

    def solve_puzzles(self):
        lines = self.load_all_input_lines()

        values = helpers.parse_all_numbers('\n'.join(lines))

        reg_a = values[0]
        reg_b = values[1]
        reg_c = values[2]
        instructions = values[3:]

        computer = ThreeBitComputer(reg_a, reg_b, reg_c, instructions)

        ans_one = ','.join(str(v) for v in computer.run())

        options = [0]
        for x in range(len(instructions), 0, -1):
            new_options = []
            target = instructions[x-1:]
            for option in options:
                next_option = 8 * option
                for new_option in range(next_option, next_option + 8):
                    computer.reset(new_option)
                    if computer.run_for_output(target):
                        new_options.append(new_option)
            options = new_options
        return ans_one, min(options)
