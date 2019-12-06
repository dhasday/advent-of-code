import hashlib

from aoc.common.day_solver import DaySolver

PUZZLE_INPUT = 'ckczppom'


class Day04Solver(DaySolver):
    year = 2015
    day = 4

    def solve_puzzles(self):
        ans_one = self._find_first_valid_hash('00000')
        ans_two = self._find_first_valid_hash('000000', start_value=ans_one)

        return ans_one, ans_two

    def _find_first_valid_hash(self, expected_prefix, start_value=0):
        cur_index = start_value
        while True:
            cur_index += 1
            md5_hex = hashlib.md5((PUZZLE_INPUT + str(cur_index)).encode()).hexdigest()

            if md5_hex.startswith(expected_prefix):
                return cur_index
