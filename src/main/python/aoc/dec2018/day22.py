from enum import Enum

from aoc.common.day_solver import DaySolver
from aoc.common.dijkstra_search import DijkstraSearch

INPUT_DEPTH = 5355
INPUT_TARGET = 14, 796

ADJACENT_OFFSETS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


class Terrain(Enum):
    ROCKY = 0
    WET = 1
    NARROW = 2


TOOL_NEITHER = 0
TOOL_TORCH = 1
TOOL_GEAR = 2


TERRAIN_TO_TOOLS = {
    Terrain.ROCKY: [TOOL_TORCH, TOOL_GEAR],
    Terrain.WET: [TOOL_NEITHER, TOOL_GEAR],
    Terrain.NARROW: [TOOL_NEITHER, TOOL_TORCH],
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
        outer_bounds = int(INPUT_TARGET[0] + 15), int(INPUT_TARGET[1] + 15)
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
        def find_adjacent_nodes(node):
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

        search = DijkstraSearch(find_adjacent_nodes)

        start_node = (start, TOOL_TORCH)
        end_nodes = [
            (target, TOOL_TORCH),
            (target, TOOL_GEAR),
        ]

        path, distance = search.find_shortest_path_to_any(start_node, end_nodes)

        return distance
