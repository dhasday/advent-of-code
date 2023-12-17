from collections import deque

from aoc.common.day_solver import DaySolver

NORTH = -1, 0
SOUTH = 1, 0
EAST = 0, 1
WEST = 0, -1


DIRECTIONs = {
    ('|', EAST): [NORTH, SOUTH],
    ('|', WEST): [NORTH, SOUTH],
    ('-', NORTH): [WEST, EAST],
    ('-', SOUTH): [WEST, EAST],
    ('/', WEST): [SOUTH],
    ('/', EAST): [NORTH],
    ('/', NORTH): [EAST],
    ('/', SOUTH): [WEST],
    ('\\', WEST): [NORTH],
    ('\\', EAST): [SOUTH],
    ('\\', NORTH): [WEST],
    ('\\', SOUTH): [EAST],
}


class Day16Solver(DaySolver):
    year = 2023
    day = 16

    size_rows = None
    size_cols = None
    mirrors = None

    def solve_puzzles(self):
        lines = self.load_all_input_lines()

        self.size_rows = len(lines)
        self.size_cols = len(lines[0])
        self.mirrors = {}
        for row, line in enumerate(lines):
            for col, val in enumerate(line):
                if val != '.':
                    self.mirrors[row, col] = val

        ans_one = None
        ans_two = 0
        for start_row in range(0, self.size_rows + 1):
            energized = self._get_energized_tiles((start_row, 0), EAST)
            if start_row == 0:
                ans_one = energized
            ans_two = max(ans_two, energized)

            energized = self._get_energized_tiles((start_row, self.size_cols - 1), WEST)
            ans_two = max(ans_two, energized)

        for start_col in range(0, self.size_cols + 1):
            energized = self._get_energized_tiles((0, start_col), SOUTH)
            ans_two = max(ans_two, energized)

            energized = self._get_energized_tiles((self.size_rows - 1, start_col), NORTH)
            ans_two = max(ans_two, energized)

        return ans_one, ans_two

    def _get_energized_tiles(self, start_pos, start_dir):
        seen = set()  # (pos, dir)
        to_check = deque()
        to_check.append((start_pos, start_dir))

        while to_check:
            cur_pos, cur_dir = to_check.popleft()
            if (cur_pos, cur_dir) in seen:
                continue

            if 0 > cur_pos[0] or cur_pos[0] >= self.size_rows:
                continue

            if 0 > cur_pos[1] or cur_pos[1] >= self.size_cols:
                continue

            seen.add((cur_pos, cur_dir))

            next_offsets = self._get_next_offsets(cur_pos, cur_dir)
            for offset in next_offsets:
                next_pos = cur_pos[0] + offset[0], cur_pos[1] + offset[1]
                to_check.append((next_pos, offset))

        return len(set(v[0] for v in seen))

    def _get_next_offsets(self, cur_pos, cur_dir):
        cur_val = self.mirrors.get(cur_pos)
        return DIRECTIONs.get((cur_val, cur_dir), [cur_dir])
