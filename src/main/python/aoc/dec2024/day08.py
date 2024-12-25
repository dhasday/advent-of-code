import math
from collections import defaultdict

from aoc.common import helpers
from aoc.common.day_solver import DaySolver


class Day08Solver(DaySolver):
    year = 2024
    day = 8

    def solve_puzzle_one(self):
        lines = self.load_all_input_lines()

        antennas_by_type = defaultdict(list)

        size_x, size_y = len(lines[0]), len(lines)

        for y, line in enumerate(lines):
            for x, val in enumerate(line):
                if val != '.':
                    antennas_by_type[val].append((x, y))

        antinodes = set()
        for nodes in antennas_by_type.values():
            antinodes.update(self._find_antinodes_p1(nodes, size_x, size_y))
        return len(antinodes)

    def solve_puzzle_two(self):
        lines = self.load_all_input_lines()

        antennas_by_type = defaultdict(list)

        size_x, size_y = len(lines[0]), len(lines)

        for y, line in enumerate(lines):
            for x, val in enumerate(line):
                if val != '.':
                    antennas_by_type[val].append((x, y))

        antinodes = set()
        for nodes in antennas_by_type.values():
            antinodes.update(self._find_antinodes_p2(nodes, size_x, size_y))
        return len(antinodes)

    def _find_antinodes_p1(self, nodes, size_x, size_y):
        antinodes = set()
        for i, node_1 in enumerate(nodes):
            for node_2 in nodes[i + 1:]:
                dx = node_1[0] - node_2[0]
                dy = node_1[1] - node_2[1]

                candidate_1 = node_1[0] + dx, node_1[1] + dy
                candidate_2 = node_2[0] - dx, node_2[1] - dy

                if self._is_in_area(candidate_1, size_x, size_y):
                    antinodes.add(candidate_1)
                if self._is_in_area(candidate_2, size_x, size_y):
                    antinodes.add(candidate_2)
        return antinodes

    def _find_antinodes_p2(self, nodes, size_x, size_y):
        antinodes = set()
        for i, node_1 in enumerate(nodes):
            for node_2 in nodes[i + 1:]:
                dx = node_1[0] - node_2[0]
                dy = node_1[1] - node_2[1]

                gcd = math.gcd(dx, dy)
                dx = dx // gcd
                dy = dy // gcd

                # Get all above
                cand = node_1[0] + dx, node_1[1] + dy
                while self._is_in_area(cand, size_x, size_y):
                    antinodes.add(cand)
                    cand = cand[0] + dx, cand[1] + dy

                cand = node_1
                while self._is_in_area(cand, size_x, size_y):
                    antinodes.add(cand)
                    cand = cand[0] - dx, cand[1] - dy
        return antinodes

    def _is_in_area(self, node, size_x, size_y):
        return 0 <= node[0] < size_x and 0 <= node[1] < size_y
