from aoc.common.day_solver import DaySolver
from aoc.common.helpers import STANDARD_DIRECTIONAL_OFFSETS


class Day04Solver(DaySolver):
    year = 2024
    day = 4

    TARGET_P2 = {'M', 'S'}

    def solve_puzzles(self):
        lines = self.load_all_input_lines()

        puzzle = {}
        x_pos = []
        a_pos = []
        for y, line in enumerate(lines):
            for x, val in enumerate(line):
                pos = x, y
                if val in 'MAS':
                    puzzle[pos] = val
                    if val == 'A':
                        a_pos.append(pos)
                elif val == 'X':
                    x_pos.append(pos)

        total_p1 = 0
        for pos in x_pos:
            for dx, dy in STANDARD_DIRECTIONAL_OFFSETS:
                if self._check_direction(puzzle, pos, dx, dy):
                    total_p1 += 1

        total_p2 = 0
        for pos in a_pos:
            up_left = puzzle.get((pos[0] - 1, pos[1] - 1))
            up_right = puzzle.get((pos[0] + 1, pos[1] - 1))
            down_left = puzzle.get((pos[0] - 1, pos[1] + 1))
            down_right = puzzle.get((pos[0] + 1, pos[1] + 1))

            d1 = {up_left, down_right}
            d2 = {up_right, down_left}

            if d1 == d2 == self.TARGET_P2:
                total_p2 += 1

        return total_p1, total_p2

    def _check_direction(self, puzzle, pos, dx, dy):
        cur_pos = pos

        for val in 'MAS':
            cur_pos = cur_pos[0] + dx, cur_pos[1] + dy
            if puzzle.get(cur_pos) != val:
                return False

        return True
