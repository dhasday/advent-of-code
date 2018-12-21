import re

INSTRUCTION_REGEX = re.compile('([a-z]{4}) (\d+) (\d+) (\d+)')


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


class ChronoProcessor(object):
    instructions = []
    registers = [0] * 6

    cur_instruction = 0
    instruction_ctr = 0

    def __init__(self, instruction_pointer):
        self.ip = instruction_pointer

    def load_instructions(self, lines):
        self.instructions = []

        for line in lines:
            parsed = INSTRUCTION_REGEX.match(line)

            instruction = [
                parsed.group(1),
                int(parsed.group(2)),
                int(parsed.group(3)),
                int(parsed.group(4)),
            ]
            self.instructions.append(instruction)

    def reset(self):
        self.cur_instruction = 0
        self.instruction_ctr = 0
        self.registers = [0] * 6

    def run_until_halt(self, debug=False):
        if not self.instructions:
            raise Exception('No instructions loaded')

        while 0 <= self.cur_instruction < len(self.instructions):
            self.execute_current_instruction(debug=debug)

    def run_until_instruction(self, ins_num, debug=False):
        if not self.instructions:
            raise Exception('No instructions loaded')

        while 0 <= self.cur_instruction < len(self.instructions):
            if ins_num == self.cur_instruction:
                return

            self.execute_current_instruction(debug=debug)

    def execute_current_instruction(self, debug=False):
        instr = self.instructions[self.cur_instruction]

        self.registers[self.ip] = self.cur_instruction
        next_registers = operations[instr[0]](self.registers, instr)

        if debug and self.cur_instruction in [5, 7, 9, 10, 11, 12]:
            self._print_tick(self.instruction_ctr, self.cur_instruction, instr, self.registers, next_registers)

        self.registers = next_registers
        self.cur_instruction = self.registers[self.ip] + 1
        self.instruction_ctr += 1

    def _print_tick(self, ctr, cur_ip, instr, old_registers, new_registers):
        msg = '{} ({:2d} {}) {} --> {}'.format(
            ctr,
            cur_ip,
            instr[0],
            old_registers,
            new_registers
        )
        print msg



