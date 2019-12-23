import re

from aoc.common.day_solver import DaySolver


class Day08Solver(DaySolver):
    year = 2015
    day = 8

    def solve_puzzle_one(self):
        escaped_regex = re.compile('\\\\(\\\\|"|x[0-9a-fA-F]{2})')

        removed_chars = 0
        for line in self.load_all_input_lines():
            cleaned_line = escaped_regex.sub('?', line[1:-1])
            removed_chars += len(line) - len(cleaned_line)

        return removed_chars

    def solve_puzzle_two(self):
        added_chars = 0
        for line in self.load_all_input_lines():
            added_chars += line.count('\\') + line.count('"') + 2

        return added_chars
