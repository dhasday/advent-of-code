from functools import cache

from aoc.common.day_solver import DaySolver


class Day11Solver(DaySolver):
    year = 2025
    day = 11

    devices = None

    def setup(self):
        lines = self.load_all_input_lines()

        self.devices = dict()
        for line in lines:
            device, rest = line.split(":")
            self.devices[device] = set(rest.strip().split(" "))

    def solve_puzzle_one(self):
        return self._find_path_count("you")

    def solve_puzzle_two(self):
        return self._find_path_count("svr", required=("fft", "dac"))

    @cache
    def _find_path_count(self, current, target="out", required=()):
        if current == target:
            # If there are any required items left, this path doesn't count
            return 1 if not required else 0

        if current in required:
            required = tuple(v for v in required if v != current)

        return sum(
            self._find_path_count(device, target, required)
            for device in self.devices[current]
        )
