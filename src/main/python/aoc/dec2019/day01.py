from aoc.common.day_solver import DaySolver

SEQUENCE_START_VALUE = 0


class Day01Solver(DaySolver):
    year = 2019
    day = 1

    def solve_puzzle_one(self):
        lines = self._load_all_input_lines()

        fuel_total = 0
        for l in lines:
            fuel_total += self._get_fuel_for_weight(int(l))
        return fuel_total

    def solve_puzzle_two(self):
        lines = self._load_all_input_lines()

        fuel_total = 0
        for l in lines:
            fuel_total += self._get_fuel_for_module(int(l))

        return fuel_total

    def _get_fuel_for_module(self, weight):
        if weight == 0:
            return 0

        fuel = self._get_fuel_for_weight(weight)
        return fuel + self._get_fuel_for_module(fuel)

    def _get_fuel_for_weight(self, weight):
        return max((weight // 3) - 2, 0)
