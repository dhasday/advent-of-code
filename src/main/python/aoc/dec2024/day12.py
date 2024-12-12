from collections import defaultdict, deque

from aoc.common import helpers
from aoc.common.day_solver import DaySolver


class Day12Solver(DaySolver):
    year = 2024
    day = 12

    def solve_puzzles(self):
        lines = self.load_all_input_lines()

        garden = defaultdict(set)

        for y, line in enumerate(lines):
            for x, val in enumerate(line):
                garden[val].add((x, y))

        regions = []
        for positions in garden.values():
            regions.extend(self._identify_regions(positions))

        total_price = 0
        bulk_price = 0
        for region in regions:
            perimeter = 0
            num_sides = 0

            # For each direction, find perimeter positions and then group into edges
            for offset in helpers.STANDARD_DIRECTIONS:
                edges = []
                for pos in region:
                    cur_pos = helpers.apply_deltas(pos, offset)
                    if cur_pos not in region:
                        edges.append(cur_pos)

                perimeter += len(edges)
                num_sides += len(self._identify_regions(edges))

            area = len(region)
            total_price += area * perimeter
            bulk_price += area * num_sides

        return total_price, bulk_price

    def _identify_regions(self, positions):
        regions = []

        remaining_positions = set(positions)

        while remaining_positions:
            cur_region = set()
            to_check = deque()

            first_pos = remaining_positions.pop()
            to_check.append(first_pos)
            while to_check:
                cur_val = to_check.popleft()
                cur_region.add(cur_val)
                for offset in helpers.STANDARD_DIRECTIONS:
                    next_val = helpers.apply_deltas(cur_val, offset)
                    if next_val in remaining_positions:
                        remaining_positions.remove(next_val)
                        to_check.append(next_val)
            regions.append(cur_region)

        return regions
