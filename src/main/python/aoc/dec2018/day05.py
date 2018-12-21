import re

from aoc.common.day_solver import DaySolver


INPUT_REGEX = re.compile('')


class Day05Solver(DaySolver):
    year = 2018
    day = 5

    def solve_puzzle_one(self):
        full_polymer = self._load_only_input_line()

        processed_polymer = self._process_polymer(full_polymer)

        return len(processed_polymer)

    def solve_puzzle_two(self):
        full_polymer = self._load_only_input_line()

        min_length = len(full_polymer)

        processed_chars = set()
        for c in full_polymer:
            char_lower = c.lower()
            if char_lower in processed_chars:
                continue

            processed_chars.add(char_lower)

            char_upper = c.upper()

            clean_polymer = full_polymer.replace(char_lower, '').replace(char_upper, '')
            processed_polymer = self._process_polymer(clean_polymer)
            if len(processed_polymer) < min_length:
                min_length = len(processed_polymer)

        return min_length

    def _load_input(self):
        return [self._load_line(l) for l in self._load_all_input_lines()]

    def _process_polymer(self, full_polymer):
        output = full_polymer
        index = 1
        while index < len(output):
            prev_char = output[index - 1]
            cur_char = output[index]

            if prev_char != cur_char and prev_char.upper() == cur_char.upper():
                output = output[:index - 1] + output[index + 1:]
                index -= 1
            else:
                index += 1

        return output

