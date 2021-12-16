from aoc.common.day_solver import DaySolver
from aoc.common.dijkstra_search import DijkstraSearch
from aoc.common.helpers import STANDARD_DIRECTIONS


class Day15Solver(DaySolver):
    year = 2021
    day = 15

    def solve_puzzle_one(self):
        lines = self.load_all_input_lines()

        size_x = len(lines[0])
        size_y = len(lines)

        risk_levels = {}
        for y in range(size_y):
            for x in range(size_x):
                risk_levels[x, y] = int(lines[y][x])

        start = 0, 0
        end = size_x - 1, size_y - 1

        search = DijkstraSearch(self._build_find_adj_nodes(risk_levels))
        _, total = search.find_shortest_path(start, end)
        return total

    def solve_puzzle_two(self):
        lines = self.load_all_input_lines()

        size_x = len(lines[0])
        size_y = len(lines)

        risk_levels = {}
        for y in range(size_y):
            for x in range(size_x):
                base_val = int(lines[y][x])
                for i in range(5):
                    for j in range(5):
                        new_val = (base_val + i + j) % 9
                        if new_val == 0:
                            new_val = 9
                        pos = x + (i * size_x), y + (j * size_y)
                        risk_levels[pos] = new_val

        max_x = max([k[0] for k in risk_levels.keys()])
        max_y = max([k[1] for k in risk_levels.keys()])

        search = DijkstraSearch(self._build_find_adj_nodes(risk_levels))
        _, total = search.find_shortest_path((0, 0), (max_x, max_y))
        return total

    def _build_find_adj_nodes(self, risk_levels):
        def _find_adj_nodes(_node):
            adj_nodes = []
            for dx, dy in STANDARD_DIRECTIONS:
                new_pos = _node[0] + dx, _node[1] + dy
                if new_pos in risk_levels:
                    adj_nodes.append((new_pos, risk_levels[new_pos]))
            return adj_nodes
        return _find_adj_nodes
