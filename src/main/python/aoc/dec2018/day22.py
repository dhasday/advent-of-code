from collections import deque

from enum import Enum

from aoc.common.day_solver import DaySolver

INPUT_DEPTH = 5355
INPUT_TARGET = 14, 796

ADJACENT_OFFSETS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


class Terrain(Enum):
    ROCKY = 0
    WET = 1
    NARROW = 2


class Tools(Enum):
    NEITHER = 0
    TORCH = 1
    GEAR = 2


TERRAIN_TO_TOOLS = {
    Terrain.ROCKY: [Tools.TORCH, Tools.GEAR],
    Terrain.WET: [Tools.NEITHER, Tools.GEAR],
    Terrain.NARROW: [Tools.NEITHER, Tools.TORCH],
}


class Day22Solver(DaySolver):
    year = 2018
    day = 22

    class Region(object):
        def __init__(self, pos, geologic_index):
            self.pos = pos
            self.geologic_index = geologic_index
            self.erosion_level = (self.geologic_index + INPUT_DEPTH) % 20183
            self.risk_level = self.erosion_level % 3
            self.terrain = Terrain(self.risk_level)

    def solve_puzzle_one(self):
        region_map = self._build_region_map(INPUT_TARGET)
        return sum([r.risk_level for r in region_map.values()])

    def solve_puzzle_two(self):
        # Wrong Answers
        # 1195
        # 1491
        # 1493 Too High
        outer_bounds = int(INPUT_TARGET[0] + 100), int(INPUT_TARGET[1] + 100)
        region_map = self._build_region_map(outer_bounds)
        return self._find_shortest_path(region_map, (0, 0), INPUT_TARGET, outer_bounds)

    def _build_region_map(self, target):
        region_map = {}

        for x in range(target[0] + 1):
            for y in range(target[1] + 1):
                self._add_region_to_map(region_map, (x, y))

        return region_map

    def _add_region_to_map(self, region_map, pos):
        if pos in region_map:
            return

        if pos == (0, 0) or pos == INPUT_TARGET:
            geologic_index = 0
        elif pos[0] == 0:
            geologic_index = pos[1] * 48271
        elif pos[1] == 0:
            geologic_index = pos[0] * 16807
        else:
            pos_one = pos[0] - 1, pos[1]
            self._add_region_to_map(region_map, pos_one)

            pos_two = pos[0], pos[1] - 1
            self._add_region_to_map(region_map, pos_two)

            geologic_index = region_map[pos_one].erosion_level * region_map[pos_two].erosion_level

        region_map[pos] = self.Region(pos, geologic_index)

    def _find_shortest_path(self, region_map, start, target, outer_edge):
        open_set = deque()
        distances = {}

        open_set.append((start, Tools.TORCH))
        ctr = 0
        min_distance_to_target = None
        target_states = [(target, t) for t in Tools]
        while open_set:
            cur_node = open_set.popleft()
            ctr += 1

            if cur_node not in distances:
                cur_distance = 0
            else:
                cur_distance = distances[cur_node]

            if min_distance_to_target and min_distance_to_target <= cur_distance:
                continue

            for n in self.find_adjacent_nodes(region_map, cur_node, outer_edge):
                node_pos = n[0]
                node_distance = cur_distance + n[1]

                if not min_distance_to_target or node_distance < min_distance_to_target:
                    if node_pos in target_states:
                        min_distance_to_target = node_distance

                    if node_pos not in distances or node_distance < distances[node_pos]:
                        distances[node_pos] = node_distance
                        open_set.append(node_pos)

        return min_distance_to_target

    def find_adjacent_nodes(self, region_map, node, outer_edge):
        pos, tool = node
        region = region_map[pos]

        adjacent_nodes = []

        # Either switch tool
        available_tools = TERRAIN_TO_TOOLS[region.terrain]
        if available_tools[0] == tool:
            adj_node = pos, available_tools[1]
            adjacent_nodes.append((adj_node, 7))
        else:
            adj_node = pos, available_tools[0]
            adjacent_nodes.append((adj_node, 7))

        # Or move to a valid adjacent node
        for offset in ADJACENT_OFFSETS:
            adjacent_pos = pos[0] + offset[0], pos[1] + offset[1]
            if adjacent_pos[0] < 0 or adjacent_pos[1] < 0 \
                    or adjacent_pos[0] > outer_edge[0] or adjacent_pos[1] > outer_edge[1]:
                continue

            adjacent_region = region_map[adjacent_pos]

            if tool in TERRAIN_TO_TOOLS[adjacent_region.terrain]:
                adj_node = adjacent_pos, tool
                adjacent_nodes.append((adj_node, 1))

        return adjacent_nodes
