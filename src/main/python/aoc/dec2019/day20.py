import math
import re
from collections import deque, defaultdict
from functools import reduce
from itertools import islice, cycle

from aoc.common.a_star_search import AStarSearch
from aoc.common.breadth_first_search import BreadthFirstSearch
from aoc.common.day_solver import DaySolver
from aoc.common.dijkstra_search import DijkstraSearch
from aoc.common.helpers import ALL_NUMBERS_REGEX, STANDARD_DIRECTIONS
from aoc.dec2019.common.intcode_processor import IntcodeProcessor


class Day20Solver(DaySolver):
    year = 2019
    day = 20

    def solve_puzzles(self):
        warps, spaces = self._load_input('20-p1')

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

        ans_one = self._solve_puzzle_one(start, end, spaces, warp_lookup)
        ans_two = self._solve_puzzle_two(start, end, spaces, warp_lookup)

        import pdb; pdb.set_trace()

        return ans_one, ans_two

    def _load_input(self, filename):
        lines = self._load_all_input_lines(filename=filename)

        warps = defaultdict(lambda: [])
        spaces = set()

        for y, row in enumerate(lines):
            for x, val in enumerate(row):
                if val == '#' or val == ' ':
                    continue

                pos = x, y
                if val == '.':
                    spaces.add(pos)
                else:
                    warps[val].append(pos)

        return warps, spaces

    def _solve_puzzle_one(self, start, end, spaces, warp_lookup):
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

    def _solve_puzzle_two(self, start_pos, end_pos, spaces, warp_lookup):
        # mappings = self._build_mappings(start_pos, end_pos, spaces, warp_lookup)
        from aoc.dec2019.day20_p2 import mappings
        import pdb;pdb.set_trace()

        def find_adjacent(cur_node):
            import pdb;
            pdb.set_trace()
            cur_pos = cur_node[0]
            cur_depth = cur_node[1]

            if cur_pos == end_pos:
                return []

            adj_nodes = []
            for next_pos, (dist, is_warp) in mappings[cur_pos].items():
                is_edge = self._is_on_edge(next_pos)

                if is_edge and cur_depth == 0:
                    continue

                if is_warp:
                    next_depth = max(0, cur_depth - 1) if is_edge else cur_depth + 1
                else:
                    next_depth = cur_depth

                next_state = next_pos, next_depth
                adj_nodes.append((next_state, dist))

            return adj_nodes

        search = BreadthFirstSearch(find_adjacent_nodes=find_adjacent)
        start = start_pos, 0
        end = end_pos, 0
        return search.find_path(start, end)

    def _build_mappings(self, start_pos, end_pos, spaces, warp_lookup):
        def find_adjacent(_pos):
            adj_nodes = []
            for offset in STANDARD_DIRECTIONS:
                next_pos = _pos[0] + offset[0], _pos[1] + offset[1]
                if next_pos in spaces \
                        or next_pos in warp_lookup \
                        or next_pos in [start_pos, end_pos]:
                    adj_nodes.append((next_pos, 1))
            return adj_nodes

        points_of_interest = [('0', start_pos), ('1', end_pos)] + list(warp_lookup.values())

        search = DijkstraSearch(find_adjacent_nodes=find_adjacent)
        mappings = defaultdict(lambda: dict())
        for warp, pos in points_of_interest:
            for w2, p2 in points_of_interest:
                if pos == p2 or p2 in mappings[pos]:
                    pass
                elif warp == w2:
                    mappings[pos].update({p2: (1, True)})
                    mappings[p2].update({pos: (1, True)})
                else:
                    result = search.find_shortest_path(pos, p2)[1]
                    if result is not None:
                        mappings[pos].update({p2: (result, False)})
                        mappings[p2].update({pos: (result, False)})

        return mappings

    def _find_distances(self, puzzle_map, start_pos):
        def get_adjacent_nodes(_node):
            adj_nodes = []

            for delta in STANDARD_DIRECTIONS:
                next_pos = delta[0] + _node[0], delta[1] + _node[1]

                if next_pos in visited:
                    continue

                if puzzle_map.is_passable(next_pos):
                    door = puzzle_map.is_door(next_pos)
                    adj_nodes.append((next_pos, door))

            return adj_nodes

        g_values = {start_pos: (0, tuple())}
        todo = [(start_pos, tuple())]
        distance = 0
        visited = set()

        while todo:
            new_todo = []
            distance += 1
            for cur_node, keys_used in todo:
                visited.add(cur_node)
                for new_node, new_key in get_adjacent_nodes(cur_node):
                    if new_node not in g_values:
                        if new_key:
                            next_keys = keys_used + tuple(new_key)
                        else:
                            next_keys = keys_used

                        new_todo.append((new_node, next_keys))
                        g_values[new_node] = (distance, next_keys)
            todo = new_todo

        return g_values

    def _is_on_edge(self, pos):
        return pos[0] in [0, 118] or pos[1] in [0, 118]
