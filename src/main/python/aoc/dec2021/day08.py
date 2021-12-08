from collections import Counter

from aoc.common.day_solver import DaySolver

DIGIT_LENGTH_MAP = {
    2: 1,
    3: 7,
    4: 4,
    7: 8,
}
SEGMENT_FREQ_MAP = {
    6: 2,
    4: 5,
    9: 6,
}


class Day08Solver(DaySolver):
    year = 2021
    day = 8

    def solve_puzzle_one(self):
        lines = self.load_all_input_lines()

        digit_count = 0
        for line in lines:
            _, output = line.split(' | ')
            for digit in output.split(' '):
                if len(digit) in [2, 3, 4, 7]:
                    digit_count += 1
        return digit_count

    def solve_puzzle_two(self):
        lines = self.load_all_input_lines()

        total = 0
        for line in lines:
            raw_digits, raw_output = line.split(' | ')

            digits = self._resolve_digits(self._split_and_sort(raw_digits))
            total += self._calculate_output(digits, self._split_and_sort(raw_output))

        return total

    def _split_and_sort(self, values):
        return [''.join(sorted(v)) for v in values.split(' ')]

    def _resolve_digits(self, raw_digits):
        digits = {}
        segments = {}
        for d in raw_digits:
            val = DIGIT_LENGTH_MAP.get(len(d))
            if val:
                digits[val] = d
        segment_counts = Counter(''.join(raw_digits))
        for s, c in segment_counts.items():
            val = SEGMENT_FREQ_MAP.get(c)
            if val:
                segments[val] = s

        segments[1] = self._missing_letter(digits[7], digits[1])
        segments[3] = self._missing_letter(digits[1], segments[6])
        segments[4] = self._missing_letter(digits[4], segments[2], segments[3], segments[6])
        segments[7] = self._missing_letter(digits[8], segments.values())

        digits[0] = self._build_digit(segments, 1, 2, 3, 5, 6, 7)
        digits[2] = self._build_digit(segments, 1, 3, 4, 5, 7)
        digits[3] = self._build_digit(segments, 1, 3, 4, 6, 7)
        digits[5] = self._build_digit(segments, 1, 2, 4, 6, 7)
        digits[6] = self._build_digit(segments, 1, 2, 4, 5, 6, 7)
        digits[9] = self._build_digit(segments, 1, 2, 3, 4, 6, 7)

        return digits

    def _calculate_output(self, digits, raw_output):
        pattern_to_digit = {v: k for k, v in digits.items()}

        total = 0
        multiplier = 1
        for v in reversed(raw_output):
            total += pattern_to_digit[v] * multiplier
            multiplier *= 10

        return total

    def _missing_letter(self, original, *all_to_remove):
        remaining = set(original)

        for to_remove in all_to_remove:
            remaining.difference_update(to_remove)

        return remaining.pop()

    def _build_digit(self, segments, *active_segments):
        return ''.join(sorted(segments[s] for s in active_segments))
