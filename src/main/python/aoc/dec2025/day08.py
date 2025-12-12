import math
from collections import defaultdict

from aoc.common import helpers
from aoc.common.day_solver import DaySolver


class Day08Solver(DaySolver):
    year = 2025
    day = 8

    def solve_puzzles(self):
        lines = self.load_all_input_lines()
        p1_target = 1000

        points = self._load_points(lines)
        distances = self._calculate_distances(points)

        p2_target = len(points)
        answer_one = 0
        answer_two = 0
        count = 0
        groups = defaultdict(set)
        for (p1, p2), distance in sorted(distances.items(), key=lambda x: x[1]):
            if count == p1_target:
                unique_groups = {tuple(v) for v in groups.values()}
                answer_one = math.prod(sorted((len(g) for g in unique_groups), reverse=True)[:3])
            count += 1

            group_1 = groups[p1]
            if p2 in group_1:
                continue
            group_1.add(p1)

            group_2 = groups[p2]
            group_2.add(p2)

            group_1.update(group_2)
            for pos in group_2:
                groups[pos] = group_1
            if len(group_1) == p2_target:
                answer_two = p1[0] * p2[0]
                break

        return answer_one, answer_two

    def _load_points(self, lines):
        points = set()
        for line in lines:
            point = tuple(helpers.parse_all_numbers(line))
            points.add(point)
        return list(points)

    def _calculate_distances(self, points):
        distances = dict()
        for idx, point_1 in enumerate(points):
            for point_2 in points[idx + 1:]:
                point_pair = tuple(sorted({point_1, point_2}))
                if point_pair not in distances:
                    distance = helpers.euclidean_distance(point_1, point_2)
                    distances[point_pair] = distance
        return distances
