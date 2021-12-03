from aoc.common.day_solver import DaySolver
from aoc.common.helpers import binary_to_decimal


class Day03Solver(DaySolver):
    year = 2021
    day = 3

    def solve_puzzle_one(self):
        lines = self.load_all_input_lines()

        line_length = len(lines[0])
        counts = [0] * line_length

        for line in lines:
            for i in range(line_length):
                if line[i] == '1':
                    counts[i] += 1

        half_lines = len(lines) / 2
        gamma_rate = 0
        epsilon_rate = 0
        cur_bit = 1
        for i in counts[::-1]:
            if i > half_lines:
                gamma_rate += cur_bit
            else:
                epsilon_rate += cur_bit

            cur_bit *= 2

        return gamma_rate * epsilon_rate

    def solve_puzzle_two(self):
        lines = self.load_all_input_lines()

        oxygen_rating = self._find_rating(lines, lambda num_on, num_off: num_on >= num_off)
        co2_rating = self._find_rating(lines, lambda num_on, num_off: num_on < num_off)

        oxygen_rating = binary_to_decimal(oxygen_rating)
        co2_rating = binary_to_decimal(co2_rating)

        return oxygen_rating * co2_rating

    def _find_rating(self, values, should_keep_on_vals):
        remaining_values = values
        idx = 0

        while len(remaining_values) > 1:
            on_values = []
            off_values = []

            for value in remaining_values:
                if value[idx] == '1':
                    on_values.append(value)
                else:
                    off_values.append(value)

            if should_keep_on_vals(len(on_values), len(off_values)):
                remaining_values = on_values
            else:
                remaining_values = off_values
            idx += 1

        return remaining_values[0]
