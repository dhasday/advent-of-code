from aoc.common.day_solver import DaySolver
from aoc.common.helpers import ALL_DIGITS_REGEX


class Day05Solver(DaySolver):
    year = 2022
    day = 5

    stacks = None
    moves = None

    def setup(self):
        lines = self.load_all_input_lines()

        self.stacks = [''] * 9
        self.moves = []
        for line in lines:
            if line.startswith('['):
                for i in range(1, len(line), 4):
                    cur = line[i]
                    if cur != ' ':
                        self.stacks[i // 4] += cur

            if line.startswith('move'):
                self.moves.append([int(v) for v in ALL_DIGITS_REGEX.findall(line)])

        for i in range(9):
            self.stacks[i] = self.stacks[i][::-1]

    def solve_puzzle_one(self):
        stacks = self.stacks.copy()

        for move in self.moves:
            count = move[0]
            orig = move[1] - 1
            target = move[2] - 1

            stacks[target] += stacks[orig][:-count - 1:-1]
            stacks[orig] = stacks[orig][:-count]

        return self._get_result(stacks)

    def solve_puzzle_two(self):
        stacks = self.stacks.copy()

        for move in self.moves:
            count = move[0]
            orig = move[1] - 1
            target = move[2] - 1

            stacks[target] += stacks[orig][-count:]
            stacks[orig] = stacks[orig][:-count]

        return self._get_result(stacks)

    def _get_result(self, stacks):
        output = ''
        for stack in stacks:
            if stack:
                output += stack[-1]

        return output
