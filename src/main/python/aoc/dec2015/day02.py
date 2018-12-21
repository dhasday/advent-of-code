import re

from aoc.common.day_solver import DaySolver

INPUT_REGEX = re.compile('(\d+)x(\d+)x(\d+)')


class Day02Solver(DaySolver):
    year = 2015
    day = 2

    def solve_puzzles(self):
        presents = self._load_input()

        ans_one = 0
        ans_two = 0

        for (l, w, h) in presents:
            a1 = l * w
            a2 = w * h
            a3 = h * l
            min_area = min([a1, a2, a3])
            ans_one += 2 * (a1 + a2 + a3)
            ans_one += min_area

            p1 = 2 * (l + w)
            p2 = 2 * (w + h)
            p3 = 2 * (h + l)
            min_parameter = min([p1, p2, p3])
            ans_two += (l * w * h)
            ans_two += min_parameter

        return ans_one, ans_two

    def _load_input(self):
        return [self._parse_line(l) for l in self._load_all_input_lines()]

    def _parse_line(self, line):
        result = INPUT_REGEX.match(line)
        return int(result.group(1)), int(result.group(2)), int(result.group(3))
