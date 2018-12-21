import re

from aoc.common.day_solver import DaySolver

INPUT = 'cqjxjnds'

INVALID_LETTERS = ['i', 'l', 'o']

DOUBLE_LETTER_REGEX = re.compile('.*([a-z])\\1.*([^\\\1])\\2.*')
SEQUENTIAL_REGEX = re.compile('.*(abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz).*')


class Day11Solver(DaySolver):
    year = 2015
    day = 11

    def solve_puzzles(self):
        password = INPUT

        password = self._advance_password(password)
        while not self._is_password_valid(password):
            password = self._advance_password(password)
        ans_one = password

        password = self._advance_password(password)
        while not self._is_password_valid(password):
            password = self._advance_password(password)
        ans_two = password

        return ans_one, ans_two

    def _generate_valid_sequences(self):
        sequences = []
        ord_a = ord('a')

        for i in range(24):
            sequences.append(chr(ord_a + i) + chr(ord_a + i + 1) + chr(ord_a + i + 2))

        return sequences

    def _is_password_valid(self, password):
        has_double_letter = DOUBLE_LETTER_REGEX.match(password)
        if has_double_letter is None:
            return False

        has_sequential_letters = SEQUENTIAL_REGEX.match(password)
        if has_sequential_letters is None:
            return False

        return True

    def _advance_password(self, cur_password):
        output = ''

        for i in range(len(cur_password) - 1, 0, -1):
            cur_letter = cur_password[i]

            # If the current letter isn't 'z' we don't need to rotate any other characters
            if cur_letter != 'z':
                next_letter = chr(ord(cur_letter) + 1)

                # Advance all following characters to the next possible valid term
                if next_letter in INVALID_LETTERS:
                    next_letter = chr(ord(cur_letter) + 2)
                    output = 'a' * (len(cur_password) - i - 1)

                return cur_password[0:i] + next_letter + output

            output = 'a' + output

        return 'ERROR'
