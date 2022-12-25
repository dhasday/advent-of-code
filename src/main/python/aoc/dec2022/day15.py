from aoc.common.day_solver import DaySolver
from aoc.common.helpers import ALL_NUMBERS_REGEX


class Day15Solver(DaySolver):
    year = 2022
    day = 15

    def solve_puzzles(self):
        lines = self.load_all_input_lines()
        p1_target = 2000000
        p2_min_bound = 0
        p2_max_bound = 4000000

        sensors = []
        for line in lines:
            values = [int(v) for v in ALL_NUMBERS_REGEX.findall(line)]
            sensor = (values[0], values[1])
            beacon = (values[2], values[3])

            dist = abs(sensor[0] - beacon[0]) + abs(sensor[1] - beacon[1])
            min_y = sensor[1] - dist
            max_y = sensor[1] + dist

            sensors.append((sensor, dist, min_y, max_y))

        ranges = self._unavailable_ranges(sensors, p1_target)
        p1 = sum(r[1] - r[0] for r in ranges)

        x = y = None
        for y in range(p2_min_bound, p2_max_bound + 1):
            ranges = self._unavailable_ranges(sensors, y)

            if len(ranges) > 1:
                x = ranges[0][1] + 1
                break
        p2 = 'Error' if x is None else (x * 4000000 + y)

        return p1, p2

    def _unavailable_ranges(self, sensors, y):
        ranges = []
        for sensor, dist, min_y, max_y in sensors:
            if y < min_y or y > max_y:
                continue
            x_dist = dist - abs(sensor[1] - y)
            ranges.append((sensor[0] - x_dist, sensor[0] + x_dist))

        ranges.sort()

        result = []
        range_low, range_high = ranges[0]
        for cur_low, cur_high in ranges[1:]:
            if cur_low - 1 <= range_high:
                range_high = max(range_high, cur_high)
            else:
                result.append((range_low, range_high))
                range_low, range_high = cur_low, cur_high
        result.append((range_low, range_high))

        return result
