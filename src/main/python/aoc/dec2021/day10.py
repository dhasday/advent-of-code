from collections import deque

from aoc.common.day_solver import DaySolver

MATCHING_CHARS = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>',
}
SCORE_MAP_INVALID = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}
SCORE_MAP_MISSING = {
    '(': 1,
    '[': 2,
    '{': 3,
    '<': 4,
}


class Day10Solver(DaySolver):
    year = 2021
    day = 10

    def solve_puzzles(self):
        lines = self.load_all_input_lines()

        invalid_total = 0
        missing_scores = []
        for line in lines:
            invalid_score, missing_score = self._validate_and_score_line(line)
            invalid_total += invalid_score
            if missing_score:
                missing_scores.append(missing_score)

        missing_middle_score = sorted(missing_scores)[len(missing_scores) // 2]
        return invalid_total, missing_middle_score

    def _validate_and_score_line(self, line):
        first_char = line[0]

        if first_char in SCORE_MAP_INVALID:
            return SCORE_MAP_INVALID[first_char[0]], None

        stack = deque()
        stack.append(first_char)
        for char in line[1:]:
            if char not in SCORE_MAP_INVALID:
                stack.append(char)
            else:
                prev_char = stack.pop()
                if MATCHING_CHARS[prev_char] != char:
                    return SCORE_MAP_INVALID[char], None

        missing_total = 0
        while stack:
            missing_total *= 5
            missing_total += SCORE_MAP_MISSING[stack.pop()]

        return 0, missing_total
