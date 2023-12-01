import re
from abc import abstractmethod, ABC

from aoc.common.day_solver import DaySolver

INSTRUCTION_REGEX = re.compile(r'(\d+|R|L)')


DIRECTION_OFFSETS = {
    (1, 0): {'L': (0, -1), 'R': (0, 1), 'val': 0},
    (0, 1): {'L': (1, 0), 'R': (-1, 0), 'val': 1},
    (-1, 0): {'L': (0, 1), 'R': (0, -1), 'val': 2},
    (0, -1): {'L': (-1, 0), 'R': (1, 0), 'val': 3},
}


class Cube:
    def __init__(self, size, lines):
        def inv(v):
            return size - 1 - v

        self.top = Side(
            size, 1, 0,
            overflow_left=lambda p: (0, inv(p[1]), 1, 0),
            overflow_right=lambda p: (0, p[1], 1, 0),
            overflow_up=lambda p: (0, p[0], 1, 0),
            overflow_down=lambda p: (p[0], 0, 0, 1),
        )
        self.bottom = Side(
            size, 1, 2,
            overflow_left=lambda p: (size - 1, p[1], -1, 0),
            overflow_right=lambda p: (size - 1, inv(p[1]), -1, 0),
            overflow_up=lambda p: (p[0], size - 1, 0, -1),
            overflow_down=lambda p: (size - 1, p[0], -1, 0),
        )
        self.left = Side(
            size, 0, 2,
            overflow_left=lambda p: (0, inv(p[1]), 1, 0),
            overflow_right=lambda p: (0, p[1], 1, 0),
            overflow_up=lambda p: (0, p[0], 1, 0),
            overflow_down=lambda p: (p[0], 0, 0, 1),
        )
        self.right = Side(
            size, 2, 0,
            overflow_left=lambda p: (size - 1, p[1], -1, 0),
            overflow_right=lambda p: (size - 1, inv(p[1]), -1, 0),
            overflow_up=lambda p: (p[0], size - 1, 0, -1),
            overflow_down=lambda p: (size - 1, p[0], -1, 0),
        )
        self.front = Side(
            size, 1, 1,
            overflow_left=lambda p: (p[1], 0, 0, 1),
            overflow_right=lambda p: (p[1], size - 1, 0, -1),
            overflow_up=lambda p: (p[0], size - 1, 0, -1),
            overflow_down=lambda p: (p[0], 0, 0, 1),
        )
        self.back = Side(
            size, 0, 3,
            overflow_left=lambda p: (p[1], 0, 0, 1),
            overflow_right=lambda p: (p[1], size - 1, 0, -1),
            overflow_up=lambda p: (p[0], size - 1, 0, -1),
            overflow_down=lambda p: (p[0], 0, 0, 1),
        )

        self.top.link_sides(self.left, self.right, self.back, self.front)
        self.bottom.link_sides(self.left, self.right, self.front, self.back)
        self.left.link_sides(self.top, self.bottom, self.front, self.back)
        self.right.link_sides(self.top, self.bottom, self.back, self.front)
        self.front.link_sides(self.left, self.right, self.top, self.bottom)
        self.back.link_sides(self.top, self.bottom, self.left, self.right)

        for x in range(0, size):
            for y in range(0, size):
                self.top.load_pos(lines, x, y)
                self.bottom.load_pos(lines, x, y)
                self.left.load_pos(lines, x, y)
                self.right.load_pos(lines, x, y)
                self.front.load_pos(lines, x, y)
                self.back.load_pos(lines, x, y)


class Side:
    left = None
    right = None
    up = None
    down = None

    def __init__(self, size, offset_x, offset_y, overflow_left, overflow_right, overflow_up, overflow_down):
        self.size = size
        self.walls = set()
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.overflow_left = overflow_left
        self.overflow_right = overflow_right
        self.overflow_up = overflow_up
        self.overflow_down = overflow_down

    def load_pos(self, lines, x, y):
        abs_pos = self.get_absolute_position((x, y))
        value = lines[abs_pos[1]][abs_pos[0]]
        if value == '#':
            self.walls.add((x, y))
        elif value != '.':
            raise Exception('Invalid pos')

    def link_sides(self, left, right, up, down):
        self.left = left
        self.right = right
        self.up = up
        self.down = down

    def move_forward(self, cur_pos, cur_dir):
        next_pos = cur_pos[0] + cur_dir[0], cur_pos[1] + cur_dir[1]
        next_dir = cur_dir
        next_side = self

        overflow = None
        if next_pos[0] < 0:
            overflow = self.overflow_left(cur_pos)
            next_side = self.left
        if next_pos[0] >= self.size:
            overflow = self.overflow_right(cur_pos)
            next_side = self.right
        if next_pos[1] < 0:
            overflow = self.overflow_up(cur_pos)
            next_side = self.up
        if next_pos[1] >= self.size:
            overflow = self.overflow_down(cur_pos)
            next_side = self.down

        if overflow:
            next_pos = overflow[0], overflow[1]
            next_dir = overflow[2], overflow[3]

        if next_pos in next_side.walls:
            return None
        else:
            return next_side, next_pos, next_dir

    def get_absolute_position(self, pos):
        return pos[0] + (self.offset_x * self.size), pos[1] + (self.offset_y * self.size)


class Day22Solver(DaySolver):
    year = 2022
    day = 22

    def solve_puzzle_one(self):
        lines = self.load_all_input_lines()

        values = {}
        for y, line in enumerate(lines):
            if line == '':
                break
            for x, c in enumerate(line):
                if c in ['.', '#']:
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
        size = 50

        cube = Cube(size, lines)
        instructions = [int(v) if v.isnumeric() else v for v in INSTRUCTION_REGEX.findall(lines[-1])]

        cur_side = cube.top
        cur_pos = 0, 0
        cur_dir = 1, 0

        for idx, ins in enumerate(instructions):
            if isinstance(ins, int):
                for i in range(ins):
                    result = cur_side.move_forward(cur_pos, cur_dir)
                    if not result:
                        break
                    cur_side, cur_pos, cur_dir = result
            else:
                cur_dir = DIRECTION_OFFSETS[cur_dir][ins]

        cur_pos = cur_side.get_absolute_position(cur_pos)
        return (cur_pos[1] + 1) * 1000 + (cur_pos[0] + 1) * 4 + DIRECTION_OFFSETS[cur_dir]['val']
