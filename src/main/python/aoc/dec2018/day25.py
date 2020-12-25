import re
from collections import deque

from aoc.common.day_solver import DaySolver

INPUT_REGEX = re.compile('(-?\d+)')


class Day25Solver(DaySolver):
    year = 2018
    day = 25

    def solve_puzzle_one(self):
        points = [tuple(map(int, INPUT_REGEX.findall(l))) for l in self.load_all_input_lines()]

        neighbors = self._find_neighbors(points)
        constellations = self._build_constellations(neighbors)

        return len(constellations)

    def solve_puzzle_two(self):
        return 'ALL DONE!'

    def _find_neighbors(self, points):
        neighbors = {p: set() for p in points}

        for idx_one, pos_one in enumerate(points):
            for pos_two in points[idx_one + 1:]:
                if self._manhattan_distance(pos_one, pos_two) <= 3:
                    neighbors[pos_one].add(pos_two)
                    neighbors[pos_two].add(pos_one)

        return neighbors

    def _manhattan_distance(self, pos_one, pos_two):
        distance = 0
        for i in range(len(pos_one)):
            distance += abs(pos_one[i] - pos_two[i])
        return distance

    def _build_constellations(self, neighbors):
        closed_set = set()

        constellations = []
        for point in neighbors:
            if point in closed_set:
                continue
            constellation = set()
            queue = deque([point])
            while queue:
                p = queue.popleft()
                if p not in constellation:
                    constellation.add(p)
                    closed_set.add(p)
                    for neighbor in neighbors[p]:
                        queue.append(neighbor)
            constellations.append(constellation)

        return constellations
