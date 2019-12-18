import math
import re
from collections import deque, defaultdict
from functools import reduce
from itertools import islice, cycle

from aoc.common.breadth_first_search import BreadthFirstSearch
from aoc.common.day_solver import DaySolver
from aoc.common.dijkstra_search import DijkstraSearch
from aoc.common.helpers import ALL_NUMBERS_REGEX, STANDARD_DIRECTIONS
from aoc.dec2019.common.intcode_processor import IntcodeProcessor


class Day18Solver(DaySolver):
    year = 2019
    day = 18

    memo = {}

    class PuzzleMap:
        def __init__(self, walls, keys, doors, starts):
            self.walls = walls
            self.keys = keys
            self.keys_inverted = {v: k for k, v in keys.items()}
            self.doors = doors
            self.doors_inverted = {v: k for k, v in doors.items()}
            self.starts = frozenset(starts)

        def is_passable(self, pos):
            return pos not in self.walls

        def is_door(self, pos):
            return self.doors_inverted.get(pos)

    def solve_puzzle_one(self):
        puzzle_map = self._load_map()
        # puzzle_map = self._load_map(filename='18-ex1')
        # puzzle_map = self._load_map(filename='18-ex2')
        # puzzle_map = self._load_map(filename='18-ex3')
        # puzzle_map = self._load_map(filename='18-ex4')

        start = list(puzzle_map.starts)[0]
        mappings = self._build_mappings(puzzle_map, start)
        return self._find_shortest_path(mappings)[1]

    def solve_puzzle_two(self):
        puzzle_map = self._load_map(filename='18-input-2')

        # mappings = [self._build_mappings(puzzle_map, s) for s in puzzle_map.starts]

        import pdb; pdb.set_trace()

        return None

    def _load_map(self, filename=None):
        lines = self._load_all_input_lines(filename=filename)

        key_values = [chr(ord('a') + i) for i in range(26)]
        door_values = [chr(ord('A') + i) for i in range(26)]
        walls = set()
        keys = {}
        doors = {}
        starts = set()
        for y, line in enumerate(lines):
            for x, val in enumerate(line):
                pos = x, y
                if val == '#':
                    walls.add(pos)
                elif val == '@':
                    starts.add(pos)
                elif val in key_values:
                    keys[val] = pos
                elif val in door_values:
                    doors[val] = pos
        return self.PuzzleMap(walls, keys, doors, starts)

    def _build_mappings(self, puzzle_map, start):
        mappings = {}
        for key, pos in list(puzzle_map.keys.items()) + list({"@": start}.items()):
            pos = tuple(pos)

            dists = self._find_distances(puzzle_map, pos)

            cur_dists = {}
            for other_key, other_pos in puzzle_map.keys.items():
                if other_key == key:
                    continue
                other_pos = tuple(other_pos)
                assert other_pos in dists
                dist, keys_needed = dists[other_pos]

                cur_dists[other_key] = (dist, frozenset(keys_needed))

            mappings[key] = cur_dists
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

    def _find_shortest_path(self, mappings):
        def _find_adjacent(node):
            if node == END:
                return []

            cur_key, collected_keys = node

            if len(collected_keys) == len(mappings.keys()) - 1:
                return [(END, 0)]

            adj_nodes = []
            for next_key, (distance, doors) in mappings[cur_key].items():
                # If we've already collected this key, skip it
                if next_key in collected_keys:
                    continue

                # If we don't have the required keys, skip it
                if len(doors - collected_keys) != 0:
                    continue

                new_keys = collected_keys | frozenset(next_key.upper())
                new_node = next_key, new_keys
                adj_nodes.append((new_node, distance))

            return adj_nodes

        START = ('@', frozenset())
        END = ('$', frozenset())

        search = DijkstraSearch(_find_adjacent)
        return search.find_shortest_path(START, END)

# key_to_key = {}
# for key, key_pos in list(keys.items()) + list({"@": cur_pos}.items()):
#     key_l = key.lower()
#     key_u = key.upper()
#     key_pos = tuple(key_pos)
#
#     dists = bfs(key_pos, expand)
#
#     cur_dists = {}
#     for other_key, other_key_pos in keys.items():
#         if other_key == key:
#             continue
#         other_key_pos = tuple(other_key_pos)
#         assert other_key_pos in dists
#         dist, keys_needed = dists[other_key_pos]
#
#         cur_dists[other_key] = (dist, frozenset(keys_needed))
#
#     key_to_key[key] = cur_dists
