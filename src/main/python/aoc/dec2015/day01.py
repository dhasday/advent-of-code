from aoc.common.day_solver import DaySolver


class Day01Solver(DaySolver):
    year = 2015
    day = 1

    def solve_puzzle_one(self):
        instructions = self.load_only_input_line()

        floor = 0
        for c in instructions:
            if c == '(':
                floor += 1
            elif c == ')':
                floor -= 1

        return floor

    def solve_puzzle_two(self):
        instructions = self.load_only_input_line()

        floor = 0
        for i in range(len(instructions)):
            c = instructions[i]

            if c == '(':
                floor += 1
            elif c == ')':
                floor -= 1

            if floor < 0:
                return i + 1

        return 'ERROR'
