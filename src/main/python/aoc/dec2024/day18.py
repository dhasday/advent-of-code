from aoc.common import helpers
from aoc.common.day_solver import DaySolver
from aoc.common.dijkstra_search import DijkstraSearch


class Day18Solver(DaySolver):
    year = 2024
    day = 18

    def solve_puzzles(self):
        lines = self.load_all_input_lines()
        size = 71
        p1_wait = 1024

        start_pos = 0, 0
        target_pos = size - 1, size - 1

        maze = dict()  # Pos: Falls at
        for i, line in enumerate(lines, start=1):
            x, y = helpers.parse_all_numbers(line)
            maze[(x, y)] = i

        _, ans_one = self._find_shortest_path(size, maze, start_pos, target_pos, p1_wait)

        non_passible = self._find_first_non_passable(size, maze, start_pos, target_pos, len(lines))
        ans_two = lines[non_passible - 1]

        return ans_one, ans_two

    def _find_shortest_path(self, size, maze, start_pos, target_pos, wait_offset):
        def _find_adj_nodes(pos):
            adj_nodes = []
            for offset in helpers.STANDARD_DIRECTIONS:
                adj_pos = helpers.apply_deltas(pos, offset)
                if 0 <= adj_pos[0] < size and 0 <= adj_pos[1] < size:
                    if adj_pos not in maze or maze[adj_pos] > wait_offset:
                        adj_nodes.append((adj_pos, 1))
            return adj_nodes

        search = DijkstraSearch(_find_adj_nodes)

        return search.find_shortest_path(start_pos, target_pos)

    def _find_first_non_passable(self, size, maze, start_pos, target_pos, max_value):
        cur_min = 0
        cur_max = max_value
        cur_test = cur_min

        while cur_min <= cur_max:
            cur_test = (cur_max + cur_min) // 2

            _, dist = self._find_shortest_path(size, maze, start_pos, target_pos, cur_test)
            if dist is None:
                cur_max = cur_test - 1
            else:
                cur_min = cur_test + 1

        return cur_test