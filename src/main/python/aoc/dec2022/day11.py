from collections import deque

from aoc.common.day_solver import DaySolver


class Day11Solver(DaySolver):
    year = 2022
    day = 11

    monkeys = None

    def setup(self):
        lines = self.load_all_input_lines()

        self.monkeys = []
        for i in range(0, len(lines), 7):
            operation = lines[i+2].split('=')[1]
            self.monkeys.append(
                Monkey(
                    lambda old, op=operation: eval(op),
                    int(lines[i+3].split(' ')[-1]),
                    int(lines[i+4].split(' ')[-1]),
                    int(lines[i+5].split(' ')[-1]),
                    [int(v) for v in lines[i+1].split(':')[1].split(',')]
                )
            )

    def solve_puzzle_one(self):
        for monkey in self.monkeys:
            monkey.reset()

        for _ in range(20):
            for monkey in self.monkeys:
                while monkey.items:
                    new_worry, target = monkey.inspect_item_part_one()
                    self.monkeys[target].items.append(new_worry)

        counts = [m.inspected_count for m in self.monkeys]
        counts = sorted(counts, reverse=True)
        return counts[0] * counts[1]

    def solve_puzzle_two(self):
        for monkey in self.monkeys:
            monkey.reset()

        max_multiple = 1
        for monkey in self.monkeys:
            max_multiple *= monkey.test

        for _ in range(10000):
            for monkey in self.monkeys:
                while monkey.items:
                    new_worry, target = monkey.inspect_item_part_two(max_multiple)
                    self.monkeys[target].items.append(new_worry)

        counts = [m.inspected_count for m in self.monkeys]
        counts = sorted(counts, reverse=True)
        return counts[0] * counts[1]


class Monkey(object):
    items = None

    def __init__(self, operation, test, if_true, if_false, starting_items):
        self.starting_items = starting_items
        self.op = operation
        self.test = test
        self.if_true = if_true
        self.if_false = if_false

        self.inspected_count = 0
        self.reset()

    def reset(self):
        self.items = deque(self.starting_items)
        self.inspected_count = 0

    def inspect_item_part_one(self):
        worry = self.op(self.items.popleft()) // 3

        target = self.if_true if worry % self.test == 0 else self.if_false
        self.inspected_count += 1
        return worry, target

    def inspect_item_part_two(self, lcm):
        worry = self.op(self.items.popleft() % lcm)

        target = self.if_true if worry % self.test == 0 else self.if_false
        self.inspected_count += 1
        return worry, target
