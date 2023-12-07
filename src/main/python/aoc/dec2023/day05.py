from collections import defaultdict

from aoc.common import helpers
from aoc.common.day_solver import DaySolver


class PlantingRange:
    def __init__(self, destination_start, origin_start, range_length):
        self.origin_start = origin_start
        self.origin_end = origin_start + range_length

        self.destination_start = destination_start
        self.destination_end = destination_start + range_length

        self.delta = destination_start - origin_start

    def __repr__(self):
        return f'O:{self.origin_start}-{self.origin_end} D:{self.delta}'


class Day05Solver(DaySolver):
    year = 2023
    day = 5

    seeds = None
    planting_map = None
    planting_ranges = None
    reverse_map = None
    reverse_ranges = None

    def setup(self):
        lines = self.load_all_input_lines()

        self.seeds = [int(v) for v in helpers.ALL_DIGITS_REGEX.findall(lines[0])]
        self.planting_map = {}
        self.planting_ranges = defaultdict(list)
        self.reverse_map = {}
        self.reverse_ranges = defaultdict(list)
        source = None
        destination = None
        for line in lines[2:]:
            if not line:
                continue
            elif ':' in line:
                split_line = line.split(' ')[0].split('-')
                source = split_line[0]
                destination = split_line[2]
            else:
                ranges = [int(v) for v in helpers.ALL_DIGITS_REGEX.findall(line)]
                self.planting_map[source] = destination
                planting_range = PlantingRange(*ranges)
                self.planting_ranges[source].append(planting_range)

                self.reverse_map[destination] = source
                self.reverse_ranges[destination].append(planting_range)

    def solve_puzzle_one(self):
        start = 'seed'
        target = 'location'

        cur_category = start
        cur_results = self.seeds
        while cur_category != target:
            cur_results = self._get_next_category(cur_category, cur_results)
            cur_category = self.planting_map[cur_category]

        return min(cur_results)

    def solve_puzzle_two(self):
        # TODO: Actually solve this
        return self._brute_force_part_two(79_000_000, 79_005_000, 1)

    def _brute_force_part_two(self, low, high, step):
        start = 'location'
        target = 'seed'

        for i in range(low, high, step):
            cur_category = start
            cur_results = [i for i in range(i, i + step)]
            while cur_category != target:
                cur_results = self._get_prev_category(cur_category, cur_results)
                cur_category = self.reverse_map[cur_category]

            if any(self._is_in_range(v) for v in cur_results):
                return i if step == 1 else f"{i}-{i + step}"

        return 'Failed'

    def _is_in_range(self, value):
        for i in range(0, len(self.seeds), 2):
            range_start = self.seeds[i]
            range_end = range_start + self.seeds[i + 1]
            if range_start <= value < range_end:
                return True
        return False

    def _get_next_category(self, category, targets):
        planting_ranges = self.planting_ranges[category]

        results = []
        for target in targets:
            next_target = None
            for planting_range in planting_ranges:
                if planting_range.origin_start <= target <= planting_range.origin_end:
                    next_target = target + planting_range.delta
                    break

            results.append(next_target if next_target is not None else target)

        return results

    def _get_prev_category(self, category, targets):
        reverse_ranges = self.reverse_ranges[category]

        results = []
        for target in targets:
            prev_target = None
            for reverse_range in reverse_ranges:
                if reverse_range.destination_start <= target < reverse_range.destination_end:
                    prev_target = target - reverse_range.delta
                    break

            results.append(prev_target if prev_target is not None else target)

        return results
