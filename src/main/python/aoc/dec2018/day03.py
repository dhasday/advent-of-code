import re

from aoc.common.day_solver import DaySolver


INPUT_REGEX = re.compile('#(\d+) @ (\d+),(\d+): (\d+)x(\d+)')


class Day03Solver(DaySolver):
    year = 2018
    day = 3

    class Measurement(object):
        def __init__(self, measurement):
            result = INPUT_REGEX.match(measurement)
            self.id = int(result.group(1))
            self.start_x = int(result.group(2))
            self.start_y = int(result.group(3))
            self.size_x = int(result.group(4))
            self.size_y = int(result.group(5))

    def solve_puzzles(self):
        measurements = self._load_all_measurements()
        fabric = dict()

        self._put_all_measurements_in_fabric(measurements, fabric)

        ans_one = self._count_overlaps_in_fabric(fabric)
        ans_two = self._find_valid_claim_id(measurements, fabric)

        return ans_one, ans_two

    def _load_all_measurements(self):
        lines = self._load_all_input_lines()

        return [self.Measurement(l) for l in lines]

    def _put_all_measurements_in_fabric(self, measurements, fabric):
        for measurement in measurements:
            for x in range(measurement.start_x, measurement.start_x + measurement.size_x):
                if x not in fabric:
                    fabric[x] = dict()
                row = fabric[x]
                for y in range(measurement.start_y, measurement.start_y + measurement.size_y):
                    if y not in row:
                        row[y] = 0
                    row[y] = row[y] + 1

    def _count_overlaps_in_fabric(self, fabric):
        count = 0

        for x in fabric:
            row = fabric[x]
            for y in row:
                col = row[y]
                if col > 1:
                    count += 1

        return count

    def _find_valid_claim_id(self, measurements, fabric):
        for measurement in measurements:
            if self._is_valid_claim(measurement, fabric):
                return measurement.id

    def _is_valid_claim(self, measurement, fabric):
        for x in range(measurement.start_x, measurement.start_x + measurement.size_x):
            for y in range(measurement.start_y, measurement.start_y + measurement.size_y):
                if fabric[x][y] != 1:
                    return False
        return True



