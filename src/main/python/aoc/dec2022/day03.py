from aoc.common.day_solver import DaySolver


class Day03Solver(DaySolver):
    year = 2022
    day = 3

    lines = []
    priority_lookup = None

    def setup(self):
        self.priority_lookup = {}
        lower_ord = ord('a')
        upper_ord = ord('A')
        for i in range(26):
            self.priority_lookup[chr(i + lower_ord)] = i + 1
            self.priority_lookup[chr(i + upper_ord)] = i + 27

        self.lines = self.load_all_input_lines()

    def solve_puzzle_one(self):
        total = 0
        for line in self.lines:
            mid = len(line) // 2
            set_one = set(line[:mid])
            set_two = set(line[mid:])

            result = set_one.intersection(set_two)
            total += self.priority_lookup[result.pop()]

        return total

    def solve_puzzle_two(self):
        total = 0
        for i in range(0, len(self.lines), 3):
            result = set(self.lines[i]).intersection(self.lines[i+1]).intersection(self.lines[i+2])
            total += self.priority_lookup[result.pop()]

        return total
