from collections import defaultdict

from aoc.common.day_solver import DaySolver


class Day10Solver(DaySolver):
    year = 2020
    day = 10

    memo = dict()

    def solve_puzzle_one(self):
        joltages = [int(line) for line in self.load_all_input_lines()]
        joltages = sorted(joltages)
        joltages.append(max(joltages) + 3)

        cur_value = 0
        differences = defaultdict(lambda: 0)
        for joltage in joltages:
            diff = joltage - cur_value
            cur_value = joltage
            differences[diff] += 1

        return differences[1] * differences[3]

    def solve_puzzle_two(self):
        joltages = {int(line) for line in self.load_all_input_lines()}

        start = 0
        target = max(joltages) + 3

        return self._count_paths(joltages, start, target)

    def _count_paths(self, joltages, current, target):
        if current == target:
            return 1
        if current > target:
            return 0
        if current not in joltages and current != 0:
            return 0

        if current in self.memo:
            return self.memo[current]

        count = 0
        count += self._count_paths(joltages, current + 1, target)
        count += self._count_paths(joltages, current + 2, target)
        count += self._count_paths(joltages, current + 3, target)
        self.memo[current] = count

        return count
