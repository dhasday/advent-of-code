from collections import defaultdict, deque
from datetime import datetime
from functools import cache
from math import inf

from aoc.common import helpers
from aoc.common.day_solver import DaySolver
from aoc.common.dijkstra_search import DijkstraSearch


class Day20Solver(DaySolver):
    year = 2024
    day = 20

    def solve_puzzles(self):
        lines = self.load_all_input_lines()

        paths = set()
        end_pos = None

        for y, line in enumerate(lines):
            for x, val in enumerate(line):
                cur_pos = x, y
                if val in ['.', 'S']:
                    paths.add(cur_pos)
                elif val == 'E':
                    end_pos = cur_pos
                    paths.add(cur_pos)

        distance_map = self._get_all_distances_from_end(paths, end_pos)

        ans_p1 = 0
        ans_p2 = 0
        for cur_pos in list(distance_map.keys()):
            ans_p1 += self._get_valid_cheat_count(distance_map, cur_pos, 2, 100)
            ans_p2 += self._get_valid_cheat_count(distance_map, cur_pos, 20, 100)
        return ans_p1, ans_p2

    def _get_all_distances_from_end(self, paths, end_pos):
        distances = defaultdict(lambda: inf)  # pos: distance

        open_set = deque()
        open_set.append((end_pos, 0))
        closed_set = set()
        while open_set:
            cur_pos, cur_dist = open_set.popleft()
            if cur_pos in closed_set:
                continue
            closed_set.add(cur_pos)
            distances[cur_pos] = cur_dist

            for offset in helpers.STANDARD_DIRECTIONS:
                adj_pos = helpers.apply_deltas(cur_pos, offset)
                if adj_pos in paths and adj_pos not in closed_set:
                    open_set.append((adj_pos, cur_dist + 1))

        return distances

    def _get_valid_cheat_count(self, distance_map, cur_pos, max_cheat_distance, min_time_save):
        total_valid_cheats = 0

        for cur_radius in range(2, max_cheat_distance + 1):
            threshold = distance_map[cur_pos] - min_time_save - cur_radius
            for offset in self.get_offsets(cur_radius):
                test_pos = helpers.apply_deltas(cur_pos, offset)
                if threshold >= distance_map[test_pos]:
                    total_valid_cheats += 1
        return total_valid_cheats

    @cache
    def get_offsets(self, radius):
        return helpers.get_manhattan_circle_offsets(radius)

Day20Solver().print_results()
