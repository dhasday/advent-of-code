from aoc.common import helpers
from aoc.common.day_solver import DaySolver
from aoc.common.lagrange import lagrange_polynomial_interpolation


class Day21Solver(DaySolver):
    year = 2023
    day = 21

    start_location = None
    rocks = None
    size_rows = None
    size_cols = None

    infinite_memo = {}  # pos: adj values

    def setup(self):
        lines = self.load_all_input_lines()

        self.start_location = None
        self.rocks = set()
        self.size_rows = len(lines)
        self.size_cols = len(lines[0])

        for row, line in enumerate(lines):
            for col, val in enumerate(line):
                cur_pos = row, col
                if val == '#':
                    self.rocks.add(cur_pos)
                elif val == 'S':
                    self.start_location = cur_pos

    def solve_puzzle_one(self):
        cur_steps = {self.start_location}
        for i in range(64):
            cur_steps = self._advance_step(cur_steps)
        return len(cur_steps)

    def solve_puzzle_two(self):
        """This is a specific solution based on the input falling into a quadratic shape of steps vs available"""
        target_steps = 26501365
        assert (target_steps - 65) % self.size_rows == 0

        cur_steps = {self.start_location}
        points = []
        for i in range(1, 65 + (2 * self.size_rows) + 1):
            cur_steps = self._advance_step_infinite(cur_steps)
            if (i - 65) % self.size_rows == 0:
                points.append((i, len(cur_steps)))

        return int(lagrange_polynomial_interpolation(target_steps, [p[0] for p in points], [p[1] for p in points]))

    def _advance_step(self, cur_steps):
        to_visit = set(cur_steps)
        can_reach = set()
        while to_visit:
            cur_pos = to_visit.pop()

            for offset in helpers.STANDARD_DIRECTIONS:
                next_pos = cur_pos[0] + offset[0], cur_pos[1] + offset[1]
                if next_pos in self.rocks:
                    continue

                if next_pos[0] < 0 or next_pos[0] >= self.size_rows:
                    continue

                if next_pos[1] < 0 or next_pos[1] >= self.size_cols:
                    continue

                can_reach.add(next_pos)

        return can_reach

    def _advance_step_infinite(self, cur_steps):
        to_visit = set(cur_steps)
        can_reach = set()
        while to_visit:
            cur_pos = to_visit.pop()

            if cur_pos not in self.infinite_memo:
                self.infinite_memo[cur_pos] = []
                for offset in helpers.STANDARD_DIRECTIONS:
                    next_pos = cur_pos[0] + offset[0], cur_pos[1] + offset[1]
                    next_pos_in_place = next_pos[0] % self.size_rows, next_pos[1] % self.size_cols
                    if next_pos_in_place not in self.rocks:
                        self.infinite_memo[cur_pos].append(next_pos)

            can_reach.update(self.infinite_memo[cur_pos])

        return can_reach
