import re
from functools import lru_cache

from aoc.common.day_solver import DaySolver

INSTRUCTION_REGEX = re.compile(r'(\d+|R|L)')


DIRECTION_OFFSETS = {
    (1, 0): {'L': (0, -1), 'R': (0, 1), 'val': 0},
    (0, 1): {'L': (1, 0), 'R': (-1, 0), 'val': 1},
    (-1, 0): {'L': (0, 1), 'R': (0, -1), 'val': 2},
    (0, -1): {'L': (-1, 0), 'R': (1, 0), 'val': 3},
}


class Day22Solver(DaySolver):
    year = 2022
    day = 22

    def setup(self):
        pass

    def solve_puzzle_one(self):
        lines = self.load_all_input_lines()

        values = {}
        for y, line in enumerate(lines):
            if line == '':
                break
            for x, c in enumerate(line):
                if c in  ['.', '#']:
                    values[(x, y)] = c
        instructions = [int(v) if v.isnumeric() else v for v in INSTRUCTION_REGEX.findall(lines[-1])]

        cur_pos = lines[0].find('.'), 0
        cur_dir = (1, 0)

        for ins in instructions:
            if isinstance(ins, int):
                for i in range(ins):
                    next_pos = cur_pos[0] + cur_dir[0], cur_pos[1] + cur_dir[1]
                    if next_pos not in values:
                        if cur_dir[0] == -1:
                            next_pos = max(v[0] for v in values if v[1] == next_pos[1]), next_pos[1]
                        elif cur_dir[0] == 1:
                            next_pos = min(v[0] for v in values if v[1] == next_pos[1]), next_pos[1]
                        elif cur_dir[1] == -1:
                            next_pos = next_pos[0], max(v[1] for v in values if v[0] == next_pos[0])
                        elif cur_dir[1] == 1:
                            next_pos = next_pos[0], min(v[1] for v in values if v[0] == next_pos[0])

                    if values[next_pos] == '#':
                        break
                    cur_pos = next_pos
            else:
                cur_dir = DIRECTION_OFFSETS[cur_dir][ins]

        return (cur_pos[1] + 1) * 1000 + (cur_pos[0] + 1) * 4 + DIRECTION_OFFSETS[cur_dir]['val']

    def solve_puzzle_two(self):
        lines = self.load_all_input_lines()

        values = {}
        for y, line in enumerate(lines):
            if line == '':
                break
            for x, c in enumerate(line):
                if c in  ['.', '#']:
                    values[(x, y)] = c
        instructions = [int(v) if v.isnumeric() else v for v in INSTRUCTION_REGEX.findall(lines[-1])]

        cur_pos = lines[0].find('.'), 0
        cur_dir = (1, 0)

        for ins in instructions:
            if isinstance(ins, int):
                for i in range(ins):
                    next_pos = cur_pos[0] + cur_dir[0], cur_pos[1] + cur_dir[1]
                    if next_pos not in values:
                        if cur_dir[0] == -1:
                            next_pos = max(v[0] for v in values if v[1] == next_pos[1]), next_pos[1]
                        elif cur_dir[0] == 1:
                            next_pos = min(v[0] for v in values if v[1] == next_pos[1]), next_pos[1]
                        elif cur_dir[1] == -1:
                            next_pos = next_pos[0], max(v[1] for v in values if v[0] == next_pos[0])
                        elif cur_dir[1] == 1:
                            next_pos = next_pos[0], min(v[1] for v in values if v[0] == next_pos[0])

                    if values[next_pos] == '#':
                        break
                    cur_pos = next_pos
            else:
                cur_dir = DIRECTION_OFFSETS[cur_dir][ins]

        return (cur_pos[1] + 1) * 1000 + (cur_pos[0] + 1) * 4 + DIRECTION_OFFSETS[cur_dir]['val']


Day22Solver().print_results()
