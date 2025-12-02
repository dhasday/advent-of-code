import re

from aoc.common.day_solver import DaySolver


REGEX_HAS_REPEAT = re.compile(r"^(\d+)(\1)+$")


class Day02Solver(DaySolver):
    year = 2025
    day = 2

    def solve_puzzles(self):
        line = self.load_only_input_line()

        answer_one = 0
        answer_two = 0
        for foo in line.split(','):
            lower, higher = foo.split('-')
            for val in range(int(lower), int(higher) + 1):
                val_str = str(val)

                if REGEX_HAS_REPEAT.fullmatch(val_str):
                    answer_two += val
                    mid = len(val_str) // 2
                    if val_str[:mid] == val_str[mid:]:
                        answer_one += val

        return answer_one, answer_two
