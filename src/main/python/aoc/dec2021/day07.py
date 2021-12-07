from aoc.common.day_solver import DaySolver
from aoc.common.helpers import ALL_NUMBERS_REGEX


class Day07Solver(DaySolver):
    year = 2021
    day = 7

    def solve_puzzle_one(self):
        line = self.load_only_input_line()
        positions = [int(v) for v in ALL_NUMBERS_REGEX.findall(line)]

        min_value = min(positions)
        max_value = max(positions)

        least_sum = sum(positions)
        for i in range(min_value, max_value + 1):
            cur_sum = 0
            for p in positions:
                cur_sum += abs(p - i)
            if cur_sum < least_sum:
                least_sum = cur_sum
        return least_sum

    def solve_puzzle_two(self):
        line = self.load_only_input_line()
        positions = [int(v) for v in ALL_NUMBERS_REGEX.findall(line)]

        min_value = min(positions)
        max_value = max(positions)

        distance_costs = {i: int((i / 2) * (1 + i)) for i in range(0, max_value + 1)}
        least_sum = None
        for i in range(min_value, max_value + 1):
            cur_sum = 0
            for p in positions:
                cur_sum += distance_costs[abs(p - i)]
            if not least_sum or cur_sum < least_sum:
                least_sum = cur_sum
        return least_sum

    def _solve_for_lease_sum(self, move_cost):
        line = self.load_only_input_line()
        positions = [int(v) for v in ALL_NUMBERS_REGEX.findall(line)]

        min_value = min(positions)
        max_value = max(positions)

        least_sum = None
        for i in range(min_value, max_value + 1):
            cur_sum = 0
            for p in positions:
                cur_sum += move_cost(abs(p - i))
            if not least_sum or cur_sum < least_sum:
                least_sum = cur_sum
        return least_sum
