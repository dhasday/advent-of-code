import re

from aoc.common.day_solver import DaySolver


INSTRUCTION_REGEX = re.compile('(do|don\'t)\(\)|mul\((\d{1,3}),(\d{1,3})\)')

class Day03Solver(DaySolver):
    year = 2024
    day = 3

    def solve_puzzles(self):
        lines = self.load_all_input_lines()

        mul_enabled = True
        total_p1 = 0
        total_p2 = 0
        for line in lines:
            matches = INSTRUCTION_REGEX.findall(line)
            for match in matches:
                if match[0] == 'do':
                    mul_enabled = True
                elif match[0] == 'don\'t':
                    mul_enabled = False
                else:
                    mul_result = int(match[1]) * int(match[2])

                    total_p1 += mul_result
                    if mul_enabled:
                        total_p2 += mul_result

        return total_p1, total_p2