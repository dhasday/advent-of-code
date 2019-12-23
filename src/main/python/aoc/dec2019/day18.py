from aoc.common.day_solver import DaySolver
from aoc.common.dijkstra_search import DijkstraSearch
from aoc.common.helpers import STANDARD_DIRECTIONS


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

        start = list(puzzle_map.starts)[0]
        mappings = self._build_mappings(puzzle_map, '@', start)
        ans_one = self._find_shortest_path_part_1(mappings, '@')[1]
        return ans_one

    def solve_puzzle_two(self):
        puzzle_map = self._load_map(filename='18-input-2')

        starts = ''
        mappings = {}
        for i, start in enumerate(puzzle_map.starts):
            start_id = str(i)
            starts += start_id
            mappings.update(self._build_mappings(puzzle_map, start_id, start))

        ans_two = self._find_shortest_path_part_2(mappings, starts)[1]
        return ans_two

    def _load_map(self, filename=None):
        lines = self.load_all_input_lines(filename=filename)

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

    def _build_mappings(self, puzzle_map, startId, start):
        mappings = {}
        for key, pos in list(puzzle_map.keys.items()) + list({startId: start}.items()):
            pos = tuple(pos)

            dists = self._find_distances(puzzle_map, pos)

            cur_dists = {}
            for other_key, other_pos in puzzle_map.keys.items():
                if other_key == key:
                    continue
                other_pos = tuple(other_pos)
                if other_pos in dists:
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

    def _find_shortest_path_part_1(self, mappings, start):
        num_keys_to_collect = len(mappings.keys()) - 1

        def _find_adjacent(node):
            if node == END:
                return []

            cur_key, collected_keys = node

            if len(collected_keys) == num_keys_to_collect:
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

        START = (start, frozenset())
        END = ('$', frozenset())

        search = DijkstraSearch(_find_adjacent)
        return search.find_shortest_path(START, END)

    def _find_shortest_path_part_2(self, mappings, starts):
        num_keys_to_collect = len(mappings.keys()) - len(starts)

        def _find_adjacent(node):
            if node == END:
                return []

            cur_keys, collected_keys = node

            if len(collected_keys) == num_keys_to_collect:
                return [(END, 0)]

            adj_nodes = []
            for cur_key in cur_keys:
                for next_key, (distance, doors) in mappings[cur_key].items():
                    # If we've already collected this key, skip it
                    if next_key in collected_keys:
                        continue

                    # If we don't have the required keys, skip it
                    if len(doors - collected_keys) != 0:
                        continue

                    new_keys = collected_keys | frozenset(next_key.upper())
                    new_node = cur_keys.replace(cur_key, next_key), new_keys
                    adj_nodes.append((new_node, distance))

            return adj_nodes

        START = (starts, frozenset())
        END = ('$', frozenset())

        search = DijkstraSearch(_find_adjacent)
        return search.find_shortest_path(START, END)
