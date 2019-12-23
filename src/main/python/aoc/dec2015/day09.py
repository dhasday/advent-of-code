import re

from aoc.common.day_solver import DaySolver

INPUT_REGEX = re.compile('(.*) to (.*) = (\d+)')


class Day09Solver(DaySolver):
    year = 2015
    day = 9

    def solve_puzzles(self):
        distances = self._load_distances()

        return self._travel_time(distances, list(distances.keys()))

    def _load_distances(self):
        distances = dict()
        for line in self.load_all_input_lines():
            parsed = INPUT_REGEX.match(line)

            place_one = parsed.group(1)
            place_two = parsed.group(2)
            distance = int(parsed.group(3))

            if place_one not in distances:
                distances[place_one] = dict()
            if place_two not in distances:
                distances[place_two] = dict()

            distances[place_one][place_two] = distance
            distances[place_two][place_one] = distance

        return distances

    def _travel_time(self, distances, remaining, current=None):
        if not remaining:
            return 0, 0

        min_total = None
        max_total = None

        for place in remaining:
            new_remaining = remaining[:]
            new_remaining.remove(place)

            place_min, place_max = self._travel_time(distances, new_remaining, place)
            if current:
                place_min += distances[current][place]
                place_max += distances[current][place]

            if min_total is None or min_total > place_min:
                min_total = place_min

            if max_total is None or place_max > max_total:
                max_total = place_max

        return min_total, max_total
