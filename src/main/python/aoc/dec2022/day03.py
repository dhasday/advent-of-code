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

    def solve_puzzle_one(self):
        lines = self.load_all_input_lines()

        total = 0
        for line in lines:
            mid = len(line) // 2
            set_one = set(line[:mid])
            set_two = set(line[mid:])

            result = set_one.intersection(set_two)
            total += self.priority_lookup[result.pop()]

        return total

    def solve_puzzle_two(self):
        lines = self.load_all_input_lines()

        total = 0
        for i in range(0, len(lines), 3):
            result = set(lines[i]).intersection(lines[i+1]).intersection(lines[i+2])
            total += self.priority_lookup[result.pop()]

        return total
