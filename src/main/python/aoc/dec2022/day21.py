import re

from aoc.common.day_solver import DaySolver


APPLY_OP = {
    '+': lambda a, b: a + b,
    '-': lambda a, b: a - b,
    '*': lambda a, b: a * b,
    '/': lambda a, b: a // b,
    '=': lambda a, b: a == b,
}

FRONT_OP = {
    '+': lambda a, b: a - b,    # b + c = a
    '-': lambda a, b: b - a,    # b - c = a
    '*': lambda a, b: a // b,   # b * c = a
    '/': lambda a, b: b // a,   # b / c = a
}
BACK_OP = {
    '+': lambda a, b: a - b,    # c + b = a
    '-': lambda a, b: a + b,    # c - b = a
    '*': lambda a, b: a // b,   # c * b = a
    '/': lambda a, b: a * b,    # c / b = a
}

MATCH_FRONT_REGEX = re.compile(r'^\((\d+)([+*/-])')
MATCH_END_REGEX = re.compile(r'([+*/-])(\d+)\)$')

ROOT_NODE = 'root'
HUMAN_NODE = 'humn'


class Monkey(object):
    val = None
    operation = None
    op_1 = None
    op_2 = None

    expanded = None

    def __init__(self, line):
        self.id, op = line.split(': ')

        if op.isnumeric():
            self.val = int(op)
        else:
            self.op_1, self.operation, self.op_2 = op.split(' ')

    def get_value(self, all_monkeys):
        if self.val is None:
            val_1 = all_monkeys[self.op_1].get_value(all_monkeys)
            val_2 = all_monkeys[self.op_2].get_value(all_monkeys)
            if self.operation in APPLY_OP:
                self.val = APPLY_OP[self.operation](val_1, val_2)
        return self.val

    def expand_operation(self, all_monkeys):
        if self.id == HUMAN_NODE:
            return HUMAN_NODE
        if not self.operation:
            return self.val
        if self.id == ROOT_NODE:
            return '{} = {}'.format(
                all_monkeys[self.op_1].expand_operation(all_monkeys),
                all_monkeys[self.op_2].expand_operation(all_monkeys),
            )
        return '({}{}{})'.format(
            all_monkeys[self.op_1].expand_operation(all_monkeys),
            self.operation,
            all_monkeys[self.op_2].expand_operation(all_monkeys),
        )


class Day21Solver(DaySolver):
    year = 2022
    day = 21

    def solve_puzzle_one(self):
        monkeys = self._load_monkeys()

        return monkeys[ROOT_NODE].get_value(monkeys)

    def solve_puzzle_two(self):
        monkeys = self._load_monkeys()
        root = monkeys[ROOT_NODE]
        root.operation = '='

        expression = monkeys[ROOT_NODE].expand_operation(monkeys)
        expression = self._simplify_expression(expression)
        return self._solve_expression(expression)

    def _load_monkeys(self):
        lines = self.load_all_input_lines()

        monkeys = {}
        for line in lines:
            monkey = Monkey(line)
            monkeys[monkey.id] = monkey

        return monkeys

    def _simplify_expression(self, expression):
        # Find each
        pattern = re.compile(r'\((\d+)([+*/-])(\d+)\)')
        while True:
            match = pattern.search(expression)
            if match:
                v1, op, v2 = match.groups()
                result = APPLY_OP[op](int(v1), int(v2))
                expression = expression[:match.start()] + str(result) + expression[match.end():]
            else:
                return expression

    def _solve_expression(self, expression):
        v1, v2 = expression.split(' = ')
        target = v1 if v1.isnumeric() else v2
        to_resolve = v1 if target == v2 else v2
        target = int(target)

        while True:
            if to_resolve == HUMAN_NODE:
                return target

            match_front = MATCH_FRONT_REGEX.search(to_resolve)
            if match_front:
                val, op = match_front.groups()
                target = FRONT_OP[op](target, int(val))
                to_resolve = to_resolve[match_front.end():-1]
                continue

            match_end = MATCH_END_REGEX.search(to_resolve)
            if match_end:
                op, val = match_end.groups()
                target = BACK_OP[op](target, int(val))
                to_resolve = to_resolve[1:match_end.start()]
                continue

            raise Exception('No valid match to ')
