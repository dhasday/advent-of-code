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
        first_win = last_win = None
        for hold_time in range(time):
            if ((time - hold_time) * hold_time) > distance:
                first_win = hold_time
                break

        for hold_time in range(time, first_win, -1):
            if ((time - hold_time) * hold_time) > distance:
                last_win = hold_time
                break

        return last_win - first_win + 1
