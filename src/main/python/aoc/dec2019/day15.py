from collections import deque

from aoc.common.day_solver import DaySolver
from aoc.common.dijkstra_search import DijkstraSearch
from aoc.dec2019.common.intcode_processor import IntcodeProcessor


NORTH = 1
SOUTH = 2
WEST = 3
EAST = 4


class Day15Solver(DaySolver):
    year = 2019
    day = 15

    def solve_puzzles(self):
        line = self._load_only_input_line()

        processor = IntcodeProcessor(line)

        grid = self._build_grid(processor)

        start = 0, 0
        end = self._find_end(grid)
        assert end is not None

        ans_one = self._find_shortest_path(grid, start, end)

        ans_two = self._spread_oxygen(grid, end)

        return ans_one, ans_two

    def _build_grid(self, processor):
        cur_pos = 0, 0
        grid = {cur_pos: (processor, 1)}

        directions = [
            (NORTH, (0, 1)),
            (SOUTH, (0, -1)),
            (WEST, (-1, 0)),
            (EAST, (1, 0)),
        ]

        open_set = deque()  # processor, cur_pos, direction
        open_set.append(cur_pos)
        ctr = 0
        while open_set:
            cur_pos = open_set.popleft()
            p1, v = grid[cur_pos]

            for dir_input, dir_offset in directions:
                next_loc = cur_pos[0] + dir_offset[0], cur_pos[1] + dir_offset[1]

                if next_loc not in grid:
                    p2 = p1.copy()
                    output = p2.get_next_output(input_value=dir_input)
                    grid[next_loc] = p2, output

                    if output != 0:
                        open_set.append(next_loc)
            ctr += 1

        return {k: v[1] for k, v in grid.items()}

    def _find_end(self, grid):
        for k, v in grid.items():
            if v == 2:
                return k
        return None

    def _find_shortest_path(self, grid, start, end):
        directions = [
            (0, 1),
            (0, -1),
            (1, 0),
            (-1, 0),
        ]

        def find_adjacent_nodes(pos):
            nodes = []
            for offset in directions:
                next_pos = pos[0] + offset[0], pos[1] + offset[1]

                if next_pos in grid and grid[next_pos] != 0:
                    nodes.append((next_pos, 1))

            return nodes

        search = DijkstraSearch(find_adjacent_nodes)
        return search.find_shortest_path(start, end)[1]

    def _spread_oxygen(self, grid, start):
        directions = [
            (0, 1),
            (0, -1),
            (1, 0),
            (-1, 0),
        ]

        remaining = sum(1 for v in grid.values() if v != 0)

        grid[start] = 'O'
        remaining -= 1

        prev_round = {start}
        closed_set = set()

        rounds = 0

        while remaining > 0:
            closed_set.update(prev_round)
            this_round = set()

            for pos in prev_round:
                for offset in directions:
                    next_pos = pos[0] + offset[0], pos[1] + offset[1]

                    if next_pos not in closed_set and next_pos in grid and grid[next_pos] == 1:
                        grid[next_pos] = 'O'
                        remaining -= 1
                        this_round.add(next_pos)

            rounds += 1
            prev_round = this_round

        return rounds
