import dataclasses
from collections import defaultdict

from aoc.common import helpers
from aoc.common.day_solver import DaySolver


@dataclasses.dataclass
class Range:
    start: int  # Inclusive
    end: int    # Exclusive

    @property
    def size(self):
        return self.end - self.start


@dataclasses.dataclass
class PlantingRange:
    origin: Range
    destination: Range

    @property
    def delta(self):
        return self.destination.start - self.origin.start

    @property
    def from_start(self):
        return self.origin.start

    @property
    def from_end(self):
        return self.origin.end


class Day05Solver(DaySolver):
    year = 2023
    day = 5

    seeds = None
    planting_map = None
    planting_ranges = None

    def setup(self):
        lines = self.load_all_input_lines()

        self.seeds = [int(v) for v in helpers.ALL_DIGITS_REGEX.findall(lines[0])]
        self.planting_map = {}
        self.planting_ranges = defaultdict(list)
        source = None
        for line in lines[2:]:
            if not line:
                continue
            elif ':' in line:
                split_line = line.split(' ')[0].split('-')
                source = split_line[0]
                self.planting_map[source] = split_line[2]
            else:
                ranges = [int(v) for v in helpers.ALL_DIGITS_REGEX.findall(line)]
                planting_range = PlantingRange(
                    Range(ranges[1], ranges[1] + ranges[2]),
                    Range(ranges[0], ranges[0] + ranges[2]),
                )
                self.planting_ranges[source].append(planting_range)

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
        start = 'seed'
        target = 'location'

        cur_ranges = []
        for i in range(0, len(self.seeds), 2):
            cur_ranges.append(Range(self.seeds[i], self.seeds[i] + self.seeds[i+1]))

        cur = start
        cur_ranges = sorted(cur_ranges, key=lambda r: r.start)
        while cur != target:
            cur_ranges = self._apply_translation_to_ranges(cur, cur_ranges)
            cur = self.planting_map[cur]

        return min(r.start for r in cur_ranges)

    def _get_next_category(self, category, targets):
        planting_ranges = self.planting_ranges[category]

        results = []
        for target in targets:
            next_target = None
            for planting_range in planting_ranges:
                if planting_range.from_start <= target < planting_range.from_end:
                    next_target = target + planting_range.delta
                    break

            results.append(next_target if next_target is not None else target)

        return results

    def _apply_translation_to_ranges(self, category, cur_ranges):
        planting_ranges = sorted(self.planting_ranges[category], key=lambda r: r.from_start)
        output = []
        # Only need to follow the planting ranges once since the ranges are sorted by start value with no overlap
        planting_idx = 0
        for cur_range in cur_ranges:
            cur_start = cur_range.start
            while cur_start < cur_range.end:
                # If we run out of planting ranges
                if planting_idx >= len(planting_ranges):
                    output.append(Range(cur_start, cur_range.end))
                    break

                planting_range = planting_ranges[planting_idx]
                if planting_range.from_end <= cur_start:
                    # If the current start is lower than the end of this range, move to the next range
                    planting_idx += 1
                elif planting_range.from_start <= cur_start:
                    # If the start falls into this range, then apply the translation
                    next_start = min(planting_range.from_end, cur_range.end)
                    output.append(Range(cur_start + planting_range.delta, next_start + planting_range.delta))
                    cur_start = next_start
                else:
                    # We're starting below the current range, so just translate to the start of it
                    next_start = min(planting_range.from_start, cur_range.end)
                    output.append(Range(cur_start, next_start))
                    cur_start = next_start

        # Sort here since the deltas could have caused this to get out of order
        return sorted(output, key=lambda r: r.start)
