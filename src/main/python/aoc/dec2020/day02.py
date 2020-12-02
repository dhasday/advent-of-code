import re

from aoc.common.day_solver import DaySolver


INPUT_PATTERN = re.compile('(\d+)-(\d+) ([a-z]): ([a-z]+)')


class Day02Solver(DaySolver):
    year = 2020
    day = 2

    def solve_puzzle_one(self):
        lines = self.load_all_input_lines()

        valid_count = 0
        for line in lines:
            result = INPUT_PATTERN.match(line)
            if not result:
                print(line)

            min_num = int(result.group(1))
            max_num = int(result.group(2))
            letter = result.group(3)
            password = result.group(4)

            if self._is_valid_sled_password(min_num, max_num, letter, password):
                valid_count += 1

        return valid_count

    def solve_puzzle_two(self):
        lines = self.load_all_input_lines()

        valid_count = 0
        for line in lines:
            result = INPUT_PATTERN.match(line)
            if not result:
                print(line)

            pos_one = int(result.group(1))
            pos_two = int(result.group(2))
            letter = result.group(3)
            password = result.group(4)

            if self._is_valid_toboggan_password(pos_one, pos_two, letter, password):
                valid_count += 1

        return valid_count

    def _is_valid_sled_password(self, min_num, max_num, letter, password):
        num_letter = 0

        for c in password:
            if c == letter:
                num_letter += 1
                if num_letter > max_num:
                    return False
        return num_letter >= min_num

    def _is_valid_toboggan_password(self, pos_one, pos_two, letter, password):
        pos_one_match = password[pos_one - 1] == letter
        pos_two_match = password[pos_two - 1] == letter

        return pos_one_match ^ pos_two_match
