import re

from common.day_solver import DaySolver

INPUT_REGEX = re.compile('(.*) (\d+),(\d+) .* (\d+),(\d+)')

INSTRUCTION_TURN_ON = 'turn on'
INSTRUCTION_TURN_OFF = 'turn off'
INSTRUCTION_TOGGLE = 'toggle'


class Day06Solver(DaySolver):
    year = 2015
    day = 6

    class Instruction(object):
        def __init__(self, line):
            result = INPUT_REGEX.match(line)

            self.instruction = result.group(1)
            self.pos_one = int(result.group(2)), int(result.group(3))
            self.pos_two = int(result.group(4)), int(result.group(5))

    def solve_puzzles(self):
        instructions = self._load_instructions()

        lights = [[False] * 1000 for _ in range(1000)]
        brightnesses = [[0] * 1000 for _ in range(1000)]

        for i in instructions:
            for x in range(i.pos_one[0], i.pos_two[0] + 1):
                for y in range(i.pos_one[1], i.pos_two[1] + 1):
                    if i.instruction == INSTRUCTION_TURN_ON:
                        lights[x][y] = True
                        brightnesses[x][y] += 1
                    elif i.instruction == INSTRUCTION_TURN_OFF:
                        lights[x][y] = False
                        brightnesses[x][y] = max(brightnesses[x][y] - 1, 0)
                    elif i.instruction == INSTRUCTION_TOGGLE:
                        lights[x][y] = not lights[x][y]
                        brightnesses[x][y] += 2

        ans_one = self._count_trues(lights)
        ans_two = self._sum_values(brightnesses)

        return ans_one, ans_two

    def _load_instructions(self):
        return [self.Instruction(l) for l in self._load_all_input_lines()]

    def _count_trues(self, field):
        count = 0
        for x in field:
            for y in x:
                if y:
                    count += 1
        return count

    def _sum_values(self, field):
        total = 0
        for x in field:
            for y in x:
                total += y
        return total
