import dataclasses
from collections import deque
from typing import Tuple

from aoc.common.breadth_first_search import BreadthFirstSearch
from aoc.common.day_solver import DaySolver
from aoc.common.dijkstra_search import DijkstraSearch

NORTH = -1, 0
SOUTH = 1, 0
EAST = 0, 1
WEST = 0, -1

VALID_DIRECTIONS = {
    NORTH: [NORTH, WEST, EAST],
    SOUTH: [SOUTH, EAST, WEST],
    EAST: [EAST, NORTH, SOUTH],
    WEST: [WEST, SOUTH, NORTH],
}


@dataclasses.dataclass
class State:
    position: Tuple[int, int]
    direction: Tuple[int, int]
    dir_count: int

    def __eq__(self, other):
        return self.position == other.position \
            and self.direction == other.direction \
            and self.dir_count == other.dir_count

    def __lt__(self, other):
        if self.position != other.position:
            return self.position < other.position
        if self.direction != other.direction:
            return self.direction < other.direction
        return self.dir_count < other.dir_count
    def __hash__(self):
        return hash(tuple([self.position, self.direction, self.dir_count]))


class Day17Solver(DaySolver):
    year = 2023
    day = 17

    heat_map = None
    size_rows = None
    size_cols = None

    def setup(self):
        lines = self.load_all_input_lines()

        self.heat_map = {}
        for row, line in enumerate(lines):
            for col, val in enumerate(line):
                self.heat_map[(row, col)] = int(val)

        self.size_rows = len(lines)
        self.size_cols = len(lines[0])

    def solve_puzzle_one(self):
        def _find_adjacent_nodes(cur_state):
            adj_positions = []

            if cur_state.dir_count == 0:
                return [
                    (State((0, 0), EAST, 1), 0),
                    (State((0, 0), SOUTH, 1), 0)
                ]

            for direction in VALID_DIRECTIONS[cur_state.direction]:
                next_pos = cur_state.position[0] + direction[0], cur_state.position[1] + direction[1]
                next_cost = self.heat_map.get(next_pos)
                if next_cost is None:
                    continue

                if cur_state.direction == direction:
                    if cur_state.dir_count < 3:
                        adj_positions.append((State(next_pos, direction, cur_state.dir_count + 1), next_cost))
                else:
                    adj_positions.append((State(next_pos, direction, 1), next_cost))

            return adj_positions

        start_pos = State((0, 0), EAST, 0)
        targets = self._get_end_targets(1, 3)

        search = DijkstraSearch(_find_adjacent_nodes)
        _, distance = search.find_shortest_path_to_any(start_pos, targets)
        return distance

    def solve_puzzle_two(self):
        def _find_adjacent_nodes(cur_state):
            adj_positions = []

            if cur_state.dir_count == 0:
                return [
                    (State((0, 0), EAST, 1), 0),
                    (State((0, 0), SOUTH, 1), 0)
                ]

            for direction in VALID_DIRECTIONS[cur_state.direction]:
                next_pos = cur_state.position[0] + direction[0], cur_state.position[1] + direction[1]
                next_cost = self.heat_map.get(next_pos)
                if next_cost is None:
                    continue

                if cur_state.direction == direction:
                    if cur_state.dir_count < 10:
                        adj_positions.append((State(next_pos, direction, cur_state.dir_count + 1), next_cost))
                elif cur_state.dir_count > 3:
                    adj_positions.append((State(next_pos, direction, 1), next_cost))

            return adj_positions

        start_pos = State((0, 0), EAST, 0)
        targets = self._get_end_targets(4, 10)

        search = DijkstraSearch(_find_adjacent_nodes)
        _, distance = search.find_shortest_path_to_any(start_pos, targets)
        return distance

    def _get_end_targets(self, min_count, max_count):
        end_pos = self.size_rows - 1, self.size_cols - 1
        targets = set()
        for i in range(min_count, max_count + 1):
            targets.add(State(end_pos, SOUTH, i))
            targets.add(State(end_pos, EAST, i))
        return targets
