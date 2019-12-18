import re

from aoc.common.day_solver import DaySolver

MIN_VALUE = 245182
MAX_VALUE = 790572


class Day04Solver(DaySolver):
    year = 2019
    day = 4

    def solve_puzzles(self):
        num_passwords_one = 0
        num_passwords_two = 0

        cur_password = MIN_VALUE
        while cur_password <= MAX_VALUE:
            cur_str = str(cur_password)

            is_increasing = self._is_increasing(cur_str)
            if cur_password != is_increasing:
                cur_password = is_increasing
                continue

            any_duplicates, exactly_two = self._has_double_digit(cur_str)
            if any_duplicates:
                num_passwords_one += 1
            if exactly_two:
                num_passwords_two += 1

            cur_password += 1

        return num_passwords_one, num_passwords_two

    def _is_increasing(self, password_str):
        prev_char = '0'
        for i in range(6):
            cur_char = password_str[i]
            if prev_char > cur_char:
                return int(password_str[0:i].ljust(6, prev_char))

            prev_char = cur_char
        return int(password_str)

    def _has_double_digit(self, password_str):
        candidates = set(re.findall(r'(\d)\1', password_str))

        for c in candidates:
            if (c * 3) not in password_str:
                return True, True

        return any(candidates), False
