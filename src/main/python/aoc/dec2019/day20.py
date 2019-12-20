from collections import defaultdict

from aoc.common.breadth_first_search import BreadthFirstSearch
from aoc.common.day_solver import DaySolver
from aoc.common.dijkstra_search import DijkstraSearch
from aoc.common.helpers import STANDARD_DIRECTIONS

INPUT_FILE = '20-p1'


class Day20Solver(DaySolver):
    year = 2019
    day = 20

    def solve_puzzle_one(self):
        start, end, spaces, warp_lookup, _, _ = self._load_input()

        def find_adjacent(cur_pos):
            adj_nodes = []

            for offset in STANDARD_DIRECTIONS:
                next_pos = cur_pos[0] + offset[0], cur_pos[1] + offset[1]
                if next_pos in spaces \
                        or next_pos in warp_lookup \
                        or next_pos == end:
                    adj_nodes.append((next_pos, 1))

            if cur_pos in warp_lookup:
                adj_nodes.append((warp_lookup[cur_pos][1], 1))

            return adj_nodes

        search = DijkstraSearch(find_adjacent)
        return search.find_shortest_path(start, end)[1]

    def solve_puzzle_two(self):
        start_pos, end_pos, spaces, warp_lookup, height, width = self._load_input()

        def is_on_edge(pos):
            return pos[0] in [0, width - 1] or pos[1] in [0, height - 1]

        def find_adjacent(cur_node):
            cur_pos, cur_depth = cur_node

            if cur_pos == end_pos and cur_depth == 0:
                return []

            adj_nodes = []
            for offset in STANDARD_DIRECTIONS:
                next_pos = cur_pos[0] + offset[0], cur_pos[1] + offset[1]
                is_edge = is_on_edge(next_pos)

                if next_pos in spaces:
                    adj_nodes.append((next_pos, cur_depth))
                elif next_pos == end_pos:
                    if cur_depth == 0:
                        adj_nodes.append((next_pos, cur_depth))
                elif next_pos in warp_lookup:
                    if not is_edge or cur_depth != 0:
                        adj_nodes.append((next_pos, cur_depth))

            if cur_pos in warp_lookup:
                is_edge = is_on_edge(cur_pos)
                new_depth = cur_depth - 1 if is_edge else cur_depth + 1

                if 0 <= new_depth <= 25:
                    adj_nodes.append((warp_lookup[cur_pos][1], new_depth))

            return adj_nodes

        search = BreadthFirstSearch(find_adjacent)
        start = start_pos, 0
        end = end_pos, 0
        return len(search.find_path(start, end)) - 1

    def _load_input(self, filename=INPUT_FILE):
        lines = self._load_all_input_lines(filename=filename)

        warps = defaultdict(lambda: [])
        spaces = set()
        height = len(lines)
        width = len(lines[0])

        for y, row in enumerate(lines):
            for x, val in enumerate(row):
                if val == '#' or val == ' ':
                    continue

                pos = x, y
                if val == '.':
                    spaces.add(pos)
                else:
                    warps[val].append(pos)

        start = warps['0'][0]
        end = warps['1'][0]
        warp_lookup = {}
        for warp, pos in warps.items():
            if warp in ('0', '1'):
                continue

            p1 = pos[0]
            p2 = pos[1]
            warp_lookup[p1] = warp, p2
            warp_lookup[p2] = warp, p1

        return start, end, spaces, warp_lookup, height, width
