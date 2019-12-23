import re
from collections import defaultdict, deque

from aoc.common.day_solver import DaySolver

INPUT_REGEX = re.compile('')


class Day20Solver(DaySolver):
    year = 2018
    day = 20

    class Bounds(object):
        def __init__(self, positions):
            self.min_x, self.min_y, self.max_x, self.max_y = [0] * 4

            for (x, y) in positions:
                if x < self.min_x:
                    self.min_x = x
                if x > self.max_x:
                    self.max_x = x
                if y < self.min_y:
                    self.min_y = y
                if y > self.max_y:
                    self.max_y = y

    class Room(object):
        north = None
        south = None
        west = None
        east = None

        def set_north(self, room):
            self.north = room
            room.south = self

        def set_south(self, room):
            self.south = room
            room.north = self

        def set_west(self, room):
            self.west = room
            room.east = self

        def set_east(self, room):
            self.east = room
            room.west = self

    def solve_puzzles(self):
        input = self.load_only_input_line().strip()[1:-1]

        rooms = defaultdict(lambda: self.Room())
        start_pos = (0, 0)
        rooms[start_pos] = self.Room()

        self._build_map(rooms, input, start_pos)
        # self._print_map(rooms)

        shortest_paths = self._find_all_shortest_path_lengths(rooms, start_pos)

        ans_one = max(shortest_paths.values())
        ans_two = len([p for p in shortest_paths if shortest_paths[p] >= 1000])

        return ans_one, ans_two

    def _build_map(self, room_map, regex, start_pos):
        cur_pos = [start_pos]
        stack = deque()
        starts, ends = cur_pos, set()

        for c in regex:
            if c == '|':
                ends.update(cur_pos)
                cur_pos = starts
            elif c == '(':
                stack.append((starts, ends))
                starts, ends = cur_pos, set()
            elif c == ')':
                starts, ends = stack.pop()
                ends.update(cur_pos)
            elif c == 'N':
                next_pos = []
                for p in cur_pos:
                    north_pos = p[0], p[1] + 1
                    room_map[p].set_north(room_map[north_pos])
                    next_pos.append(north_pos)
                cur_pos = next_pos
            elif c == 'S':
                next_pos = []
                for p in cur_pos:
                    south_pos = p[0], p[1] - 1
                    room_map[p].set_south(room_map[south_pos])
                    next_pos.append(south_pos)
                cur_pos = next_pos
            elif c == 'W':
                next_pos = []
                for p in cur_pos:
                    west_pos = p[0] - 1, p[1]
                    room_map[p].set_west(room_map[west_pos])
                    next_pos.append(west_pos)
                cur_pos = next_pos
            elif c == 'E':
                next_pos = []
                for p in cur_pos:
                    east_pos = p[0] + 1, p[1]
                    room_map[p].set_east(room_map[east_pos])
                    next_pos.append(east_pos)
                cur_pos = next_pos
            else:
                raise Exception('Encountered invalid character: ' + c)

    def _print_map(self, rooms):
        bounds = self.Bounds(rooms.keys())
        size_x = (bounds.max_x - bounds.min_x) * 2 + 3

        print('#' * size_x)

        for y in range(bounds.max_y, bounds.min_y - 1, -1):
            cur_row = '#'
            doors_row = '#'
            for x in range(bounds.min_x, bounds.max_x + 1):
                pos = (x, y)
                if pos in rooms:
                    room = rooms[pos]
                    cur_row += '  ' if room.east else ' #'
                    doors_row += ' #' if room.south else '##'
                else:
                    cur_row += '##'
                    doors_row += '##'
            print(cur_row)
            print(doors_row)

    def _find_all_shortest_path_lengths(self, rooms, start_pos):
        def find_adjacent_nodes(pos):
            room = rooms[pos]

            nodes = []
            if room.north:
                north_pos = pos[0], pos[1] + 1
                nodes.append(north_pos)
            if room.south:
                south_pos = pos[0], pos[1] - 1
                nodes.append(south_pos)
            if room.west:
                west_pos = pos[0] - 1, pos[1]
                nodes.append(west_pos)
            if room.east:
                east_pos = pos[0] + 1, pos[1]
                nodes.append(east_pos)
            return nodes

        path_lengths = {}

        open_set = deque()

        open_set.append(start_pos)

        while open_set:
            cur_pos = open_set.popleft()

            if cur_pos in path_lengths:
                continue

            adjacent_nodes = find_adjacent_nodes(cur_pos)
            min_distance = None
            for node in adjacent_nodes:
                if node in path_lengths:
                    node_distance = path_lengths[node]
                    if min_distance is None or node_distance < min_distance:
                        min_distance = path_lengths[node]
                else:
                    open_set.append(node)
            if cur_pos == start_pos:
                min_distance = -1

            path_lengths[cur_pos] = min_distance + 1

        return path_lengths
