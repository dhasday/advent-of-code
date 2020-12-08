import re

INSTRUCTION_REGEX = re.compile(r'([a-z]+) ([+-])(\d+)')

INS_NOOP = 'nop'
INS_JUMP = 'jmp'
INS_ACCUMULATE = 'acc'


class GameConsole(object):
    def __init__(self, instructions):
        self.instructions = [Instruction(instruction) for instruction in instructions]

        self.cur_ins = 0
        self.acc = 0
        self.exit_ins = len(self.instructions)
        self.visited = set()

    def reset(self):
        self.cur_ins = 0
        self.acc = 0
        self.visited.clear()

    def run_until_stop(self, can_repeat=False):
        self.acc = 0
        self.cur_ins = 0

        while self.cur_ins < self.exit_ins and (can_repeat or self.cur_ins not in self.visited):
            self.visited.add(self.cur_ins)
            ins = self.instructions[self.cur_ins]
            self.cur_ins, self.acc = ins.process(self.cur_ins, self.acc)

        return self.acc

    def get_instruction(self, num):
        return self.instructions[num]


class Instruction(object):
    def __init__(self, line):
        result = INSTRUCTION_REGEX.match(line)

        self.ins = result.group(1)
        self.arg_1 = int(result.group(3))

        if result.group(2) == '-':
            self.arg_1 *= -1

    def process(self, cur_ins, acc):
        if self.ins == INS_NOOP:
            return cur_ins + 1, acc

        if self.ins == INS_ACCUMULATE:
            return cur_ins + 1, acc + self.arg_1

        if self.ins == INS_JUMP:
            return cur_ins + self.arg_1, acc

        raise Exception('Unknown instruction: ' + self.ins)

    def alter_instruction(self):
        if self.ins == INS_ACCUMULATE:
            return False

        self.ins = INS_JUMP if self.ins == INS_NOOP else INS_NOOP
        return True

    def __str__(self):
        return '{} {}'.format(self.ins, self.arg_1)

    __unicode__ = __str__
