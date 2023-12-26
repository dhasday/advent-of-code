from enum import Enum

from aoc.common.day_solver import DaySolver


class Direction(Enum):
    NORTH = 1
    WEST = 2
    SOUTH = 3
    EAST = 4


PIPE_NORTH_SOUTH = '|'
PIPE_EAST_WEST = '-'
PIPE_NORTH_EAST = 'L'
PIPE_NORTH_WEST = 'J'
PIPE_SOUTH_WEST = '7'
PIPE_SOUTH_EAST = 'F'

CONNECTIONS = {
    PIPE_NORTH_SOUTH: {Direction.NORTH, Direction.SOUTH},
    PIPE_EAST_WEST: {Direction.EAST, Direction.WEST},
    PIPE_NORTH_EAST: {Direction.NORTH, Direction.EAST},
    PIPE_NORTH_WEST: {Direction.NORTH, Direction.WEST},
    PIPE_SOUTH_EAST: {Direction.SOUTH, Direction.EAST},
    PIPE_SOUTH_WEST: {Direction.SOUTH, Direction.WEST},
}
OPPOSITE_DIRECTION_MAP = {
    Direction.NORTH: Direction.SOUTH,
    Direction.SOUTH: Direction.NORTH,
    Direction.EAST: Direction.WEST,
    Direction.WEST: Direction.EAST,
}

CONNECTION_OFFSET = {
    Direction.NORTH: (-1, 0),
    Direction.WEST: (0, -1),
    Direction.SOUTH: (1, 0),
    Direction.EAST: (0, 1),
}


class Day10Solver(DaySolver):
    year = 2023
    day = 10

    def solve_puzzles(self):
        lines = self.load_all_input_lines()

        start = None
        pipes = {}
        for row, line in enumerate(lines):
            for col, char in enumerate(line):
                if char != '.':
                    pipes[row, col] = char
                if char == 'S':
                    start = (row, col)

        start_symbol = self._determine_start_symbol(start, pipes)

        loop_size, loop = self._find_longest_loop(start, pipes)
        ans_one = loop_size // 2

        clean_grid = self._create_clean_grid(start_symbol, loop, pipes, start)
        ans_two = self._count_included_cells(clean_grid)
        return ans_one, ans_two

    def _determine_start_symbol(self, start, pipes):
        valid_dirs = set()
        for cur_dir in Direction:
            next_pos = self._add_offset(start, CONNECTION_OFFSET[cur_dir])
            if next_pos in pipes and self._can_enter(pipes[next_pos], cur_dir):
                valid_dirs.add(cur_dir)

        for symbol, connects in CONNECTIONS.items():
            if valid_dirs == connects:
                return symbol

        return None

    def _find_longest_loop(self, start, pipes):
        max_length = 0
        max_loop = None

        for start_dir in Direction:
            dir_length, loop = self._get_loop_size(pipes, start, start_dir)
            if dir_length > max_length:
                max_length = dir_length
                max_loop = loop

        return max_length, max_loop

    def _get_loop_size(self, pipes, start, start_dir):
        size = 0
        seen = set()
        cur_pos = start
        cur_dir = start_dir
        while cur_pos not in seen:
            seen.add(cur_pos)
            next_pos = self._add_offset(cur_pos, CONNECTION_OFFSET[cur_dir])

            if next_pos == start:
                cur_pos = next_pos
                size += 1
            elif next_pos in pipes and self._can_enter(pipes[next_pos], cur_dir):
                cur_dir = self._get_next_dir(pipes[next_pos], cur_dir)
                cur_pos = next_pos
                size += 1
            else:
                return -1, None

        if cur_pos != start:
            return -1, None

        return size, seen

    def _add_offset(self, pos, offset):
        return pos[0] + offset[0], pos[1] + offset[1]

    def _can_enter(self, pipe, from_direction):
        return OPPOSITE_DIRECTION_MAP[from_direction] in CONNECTIONS[pipe]

    def _get_next_dir(self, pipe, cur_dir):
        return next(v for v in CONNECTIONS[pipe] if v != OPPOSITE_DIRECTION_MAP[cur_dir])

    def _create_clean_grid(self, start_symbol, loop, pipes, start):
        max_row = max(p[0] for p in loop)
        max_col = max(p[1] for p in loop)
        clean_grid = ['.' * (max_col + 1)] * (max_row + 1)
        for pos in loop:
            char = start_symbol if pos == start else pipes[pos]

            cur_row = clean_grid[pos[0]]
            clean_grid[pos[0]] = cur_row[:pos[1]] + char + cur_row[pos[1] + 1:]
        return clean_grid

    def _count_included_cells(self, clean_grid):
        count = 0
        for row in clean_grid:
            north_count = 0
            for char in row:
                # We're only within the loop if there is an odd number of north pipes
                if char in [PIPE_NORTH_SOUTH, PIPE_NORTH_WEST, PIPE_NORTH_EAST]:
                    north_count += 1
                elif char == '.' and north_count % 2 == 1:
                    count += 1
        return count
