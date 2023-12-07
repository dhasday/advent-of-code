import dataclasses

from aoc.common import helpers
from aoc.common.day_solver import DaySolver


DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']


@dataclasses.dataclass
class PartNumber:
    number: int
    row: int
    start_col: int
    end_col: int

    include: bool = False
    part_locations: set[tuple[int, int]] = None
    adj_locations: set[tuple[int, int]] = None

    def get_part_locations(self):
        if self.part_locations is None:
            self.part_locations = set()
            for cur_col in range(self.start_col, self.end_col + 1):
                self.part_locations.add((self.row, cur_col))
        return self.part_locations

    def get_adj_locations(self):
        if self.adj_locations is None:
            self.adj_locations = set()
            for cur_col in range(self.start_col - 1, self.end_col + 2):
                self.adj_locations.add((self.row - 1, cur_col))
                self.adj_locations.add((self.row, cur_col))
                self.adj_locations.add((self.row + 1, cur_col))
        return self.adj_locations


class Day03Solver(DaySolver):
    year = 2023
    day = 3

    def setup(self):
        lines = self.load_all_input_lines()

        self.parts = []  # PartNumber
        self.symbols = {}  # loc_row, loc_col: symbol
        for row_idx, line in enumerate(lines):
            cur_number = ''
            start_idx = end_idx = None
            cur_idx = 0
            while cur_idx < len(line):
                cur_char = line[cur_idx]
                if cur_char in DIGITS:
                    if cur_number == '':
                        start_idx = cur_idx
                    cur_number += cur_char
                    end_idx = cur_idx
                elif cur_number != '':
                    self.parts.append(PartNumber(int(cur_number), row_idx, start_idx, end_idx))
                    cur_number = ''

                if cur_char not in DIGITS and cur_char != '.':
                    self.symbols[row_idx, cur_idx] = cur_char

                cur_idx += 1

            if cur_number != '':
                self.parts.append(PartNumber(int(cur_number), row_idx, start_idx, end_idx))

    def solve_puzzle_one(self):
        # 4361 Too Low
        ans_one = 0
        for part in self.parts:
            for adj_loc in part.get_adj_locations():
                if adj_loc in self.symbols:
                    ans_one += part.number
                    break
        return ans_one

    def solve_puzzle_two(self):
        ans_two = 0
        for loc, symbol in self.symbols.items():
            if symbol == '*':
                adj_parts = self._find_adj_parts(loc)
                if len(adj_parts) == 2:
                    ans_two += (adj_parts[0].number * adj_parts[1].number)

        return ans_two

    def _find_adj_parts(self, loc):
        loc_adj = {(loc[0] + dx, loc[1] + dy) for dx, dy in helpers.STANDARD_DIRECTIONAL_OFFSETS}

        adj_parts = []
        for part in self.parts:
            if abs(part.row - loc[0]) > 1:
                continue

            if loc_adj.intersection(part.get_part_locations()):
                adj_parts.append(part)

        return adj_parts
