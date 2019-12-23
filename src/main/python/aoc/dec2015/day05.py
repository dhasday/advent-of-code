import re

from aoc.common.day_solver import DaySolver


class Day05Solver(DaySolver):
    year = 2015
    day = 5

    def solve_puzzle_one(self):
        three_vowels = re.compile('.*[aeiou].*[aeiou].*[aeiou].*')
        double_letter = re.compile('.*([a-z])\\1.*')
        invalid_strings = re.compile('.*(ab|cd|pq|xy).*')

        values = self.load_all_input_lines()
        valid_count = 0
        for v in values:
            if three_vowels.match(v) is not None \
                    and double_letter.match(v) is not None \
                    and invalid_strings.match(v) is None:
                valid_count += 1

        return valid_count

    def solve_puzzle_two(self):
        double_repeat = re.compile('.*([a-z][a-z]).*\\1.*')
        split_repeat = re.compile('.*([a-z]).\\1.*')

        values = self.load_all_input_lines()

        valid_count = 0
        for v in values:
            if double_repeat.match(v) is not None \
                    and split_repeat.match(v) is not None:
                valid_count += 1

        return valid_count
