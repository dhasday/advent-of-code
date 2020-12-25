from aoc.common.day_solver import DaySolver

MODULUS = 20201227
START_VALUE = 1
SUBJECT_NUMBER = 7


class Day25Solver(DaySolver):
    year = 2020
    day = 25

    def solve_puzzle_one(self):
        lines = self.load_all_input_lines()

        public_key_1 = int(lines[0])
        public_key_2 = int(lines[1])
        num_loops, subject_number = self._get_smaller_loop_size(public_key_1, public_key_2)

        # Apply Diffie-Hellman
        return pow(subject_number, num_loops, MODULUS)

    def solve_puzzle_two(self):
        return 'ALL DONE!'

    def _get_smaller_loop_size(self, key_1, key_2):
        cur_value = START_VALUE

        cur_loop = 1
        while True:
            cur_value = self._apply_transform(SUBJECT_NUMBER, MODULUS, cur_value)

            if cur_value == key_1:
                return cur_loop, key_2
            if cur_value == key_2:
                return cur_loop, key_1

            cur_loop += 1

    def _apply_transform(self, subject_number, modulus, cur_value):
        return (cur_value * subject_number) % modulus
