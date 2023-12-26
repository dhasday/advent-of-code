import heapq

import networkx as nx

from aoc.common import helpers
from aoc.common.day_solver import DaySolver

SLOPE_OFFSET = {
    '<': [(0, -1)],
    '^': [(-1, 0)],
    '>': [(0, 1)],
    'v': [(1, 0)],
}

SLOPE = '<^>v'
PATH = '.'
WALKABLE = PATH + SLOPE


class Day23Solver(DaySolver):
    year = 2023
    day = 23

    lines = None
    start = None
    target = None
    junctions = None

    def setup(self):
        self.lines = self.load_all_input_lines()

        self.start = 0, self.lines[0].index('.')
        self.target = len(self.lines) - 1, self.lines[-1].index('.')

        self.junctions = set()

        for row, line in enumerate(self.lines[1:-1], start=1):
            for col, value in enumerate(line):
                if value in WALKABLE:
                    neighbors = 0
                    for offset in helpers.STANDARD_DIRECTIONS:
                        next_row = row + offset[0]
                        next_col = col + offset[1]
                        if 0 <= next_col < len(self.lines[0]) and self.lines[next_row][next_col] in WALKABLE:
                            neighbors += 1
                    if neighbors > 2:
                        self.junctions.add((row, col))
        self.junctions.add(self.start)
        self.junctions.add(self.target)

    def solve_puzzle_one(self):
        linked_junctions = self._link_junctions(follow_slopes=True)
        return self._build_graph_and_solve(linked_junctions)

    def solve_puzzle_two(self):
        linked_junctions = self._link_junctions(follow_slopes=False)
        return self._build_graph_and_solve(linked_junctions)

    def _link_junctions(self, follow_slopes):
        def get_adj_nodes(pos):
            if follow_slopes:
                offsets = SLOPE_OFFSET.get(self.lines[pos[0]][pos[1]], helpers.STANDARD_DIRECTIONS)
            else:
                offsets = helpers.STANDARD_DIRECTIONS

            adj_nodes = []
            for offset in offsets:
                next_pos = pos[0] + offset[0], pos[1] + offset[1]
                if 0 <= next_pos[0] < len(self.lines) \
                        and 0 <= next_pos[1] < len(self.lines[0]) \
                        and self.lines[next_pos[0]][next_pos[1]] in WALKABLE:
                    adj_nodes.append(next_pos)
            return adj_nodes

        linked = {}
        for junction in self.junctions:
            linked[junction] = {}

            open_set = []
            closed_set = dict()

            heapq.heappush(open_set, (0, junction))
            closed_set[junction] = (junction, 0)
            while open_set:
                cur_dist, cur_pos = heapq.heappop(open_set)

                cur_node = closed_set.get(cur_pos)
                if cur_node[1] < cur_dist:
                    continue

                for adj_pos in get_adj_nodes(cur_pos):
                    if adj_pos in closed_set:
                        continue

                    if adj_pos in self.junctions:
                        linked[junction][adj_pos] = cur_dist + 1
                    else:
                        closed_set[adj_pos] = (adj_pos, cur_dist + 1)
                        heapq.heappush(open_set, (cur_dist + 1, adj_pos))

        return linked

    def _build_graph_and_solve(self, linked_junctions):
        graph = nx.DiGraph()
        for j1, links in linked_junctions.items():
            for j2, dist in links.items():
                graph.add_edge(j1, j2, weight=dist)

        max_length = -1
        for path in nx.all_simple_paths(graph, self.start, self.target):
            total = 0
            cur_node = path[0]
            for next_node in path[1:]:
                total += graph.get_edge_data(cur_node, next_node).get('weight')
                cur_node = next_node
            max_length = max(max_length, total)
        return max_length
