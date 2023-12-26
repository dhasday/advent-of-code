from aoc.common import helpers
from aoc.common.day_solver import DaySolver


class Day06Solver(DaySolver):
    year = 2023
    day = 6

    def solve_puzzle_one(self):
        lines = self.load_all_input_lines()

        times = [int(v) for v in helpers.ALL_DIGITS_REGEX.findall(lines[0])]
        distances = [int(v) for v in helpers.ALL_DIGITS_REGEX.findall(lines[1])]

        ans_one = 1
        for time, distance in zip(times, distances):
            ans_one *= self._get_num_wins(time, distance)

        return ans_one

    def solve_puzzle_two(self):
        lines = self.load_all_input_lines()

        times = [int(v) for v in helpers.ALL_DIGITS_REGEX.findall(lines[0].replace(' ', ''))]
        distances = [int(v) for v in helpers.ALL_DIGITS_REGEX.findall(lines[1].replace(' ', ''))]

        return self._get_num_wins(times[0], distances[0])

    def _get_num_wins(self, time, distance):
        min_value = 0
        max_value = time // 2

        if self._get_distance(time, max_value) < distance:
            return 0

        # Binary search for min value
        while min_value + 1 < max_value:
            cur = (min_value + max_value) // 2
            if self._get_distance(time, cur) > distance:
                max_value = cur
            else:
                min_value = cur
        first_win = min_value + 1

        # Calculate last win because the distance graph is quadratic
        last_win = (time / 2) + (time / 2 - first_win)

        return int(last_win - first_win + 1)

    def _get_distance(self, time, hold_time):
        return (time - hold_time) * hold_time
