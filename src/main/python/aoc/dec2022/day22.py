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
        self.top = TopSide(size, 1, 0)
        self.bottom = BottomSide(size, 1, 2)
        self.left = LeftSide(size, 0, 2)
        self.right = RightSide(size, 2, 0)
        self.front = FrontSide(size, 1, 1)
        self.back = BackSide(size, 0, 3)

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


class Side(ABC):
    left = None
    right = None
    up = None
    down = None

    def __init__(self, size, offset_x, offset_y):
        self.size = size
        self.walls = set()
        self.offset_x = offset_x
        self.offset_y = offset_y

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

        if next_pos[0] < 0:
            next_side, next_pos, next_dir = self.overflow_left(cur_pos)
        if next_pos[0] >= self.size:
            next_side, next_pos, next_dir = self.overflow_right(cur_pos)
        if next_pos[1] < 0:
            next_side, next_pos, next_dir = self.overflow_up(cur_pos)
        if next_pos[1] >= self.size:
            next_side, next_pos, next_dir = self.overflow_down(cur_pos)

        if next_pos in next_side.walls:
            return None
        else:
            return next_side, next_pos, next_dir

    def get_absolute_position(self, pos):
        return pos[0] + (self.offset_x * self.size), pos[1] + (self.offset_y * self.size)

    def _invert_side(self, cur_val):
        return self.size - 1 - cur_val

    @abstractmethod
    def overflow_left(self, cur_pos):
        pass

    @abstractmethod
    def overflow_right(self, cur_pos):
        pass

    @abstractmethod
    def overflow_up(self, cur_pos):
        pass

    @abstractmethod
    def overflow_down(self, cur_pos):
        pass


class TopSide(Side):
    def overflow_left(self, cur_pos):
        next_pos = 0, self._invert_side(cur_pos[1])
        next_dir = 1, 0
        return self.left, next_pos, next_dir

    def overflow_right(self, cur_pos):
        next_pos = 0, cur_pos[1]
        next_dir = 1, 0
        return self.right, next_pos, next_dir

    def overflow_up(self, cur_pos):
        next_pos = 0, cur_pos[0]
        next_dir = 1, 0
        return self.up, next_pos, next_dir

    def overflow_down(self, cur_pos):
        next_pos = cur_pos[0], 0
        next_dir = 0, 1
        return self.down, next_pos, next_dir


class FrontSide(Side):
    def overflow_left(self, cur_pos):
        next_pos = cur_pos[1], 0
        next_dir = 0, 1
        return self.left, next_pos, next_dir

    def overflow_right(self, cur_pos):
        next_pos = cur_pos[1], self.size - 1
        next_dir = 0, -1
        return self.right, next_pos, next_dir

    def overflow_up(self, cur_pos):
        next_pos = cur_pos[0], self.size - 1
        next_dir = 0, -1
        return self.up, next_pos, next_dir

    def overflow_down(self, cur_pos):
        next_pos = cur_pos[0], 0
        next_dir = 0, 1
        return self.down, next_pos, next_dir


class RightSide(Side):
    def overflow_left(self, cur_pos):
        next_pos = self.size - 1, cur_pos[1]
        next_dir = -1, 0
        return self.left, next_pos, next_dir

    def overflow_right(self, cur_pos):
        next_pos = self.size - 1, self._invert_side(cur_pos[1])
        next_dir = -1, 0
        return self.right, next_pos, next_dir

    def overflow_up(self, cur_pos):
        next_pos = cur_pos[0], self.size - 1
        next_dir = 0, -1
        return self.up, next_pos, next_dir

    def overflow_down(self, cur_pos):
        next_pos = self.size - 1, cur_pos[0]
        next_dir = -1, 0
        return self.down, next_pos, next_dir


class LeftSide(Side):
    def overflow_left(self, cur_pos):
        next_pos = 0, self._invert_side(cur_pos[1])
        next_dir = 1, 0
        return self.left, next_pos, next_dir

    def overflow_right(self, cur_pos):
        next_pos = 0, cur_pos[1]
        next_dir = 1, 0
        return self.right, next_pos, next_dir

    def overflow_up(self, cur_pos):
        next_pos = 0, cur_pos[0]
        next_dir = 1, 0
        return self.up, next_pos, next_dir

    def overflow_down(self, cur_pos):
        next_pos = cur_pos[0], 0
        next_dir = 0, 1
        return self.down, next_pos, next_dir


class BottomSide(Side):
    def overflow_left(self, cur_pos):
        next_pos = self.size - 1, cur_pos[1]
        next_dir = -1, 0
        return self.left, next_pos, next_dir

    def overflow_right(self, cur_pos):
        next_pos = self.size - 1, self._invert_side(cur_pos[1])
        next_dir = -1, 0
        return self.right, next_pos, next_dir

    def overflow_up(self, cur_pos):
        next_pos = cur_pos[0], self.size - 1
        next_dir = 0, -1
        return self.up, next_pos, next_dir

    def overflow_down(self, cur_pos):
        next_pos = self.size - 1, cur_pos[0]
        next_dir = -1, 0
        return self.down, next_pos, next_dir


class BackSide(Side):
    def overflow_left(self, cur_pos):
        next_pos = cur_pos[1], 0
        next_dir = 0, 1
        return self.left, next_pos, next_dir

    def overflow_right(self, cur_pos):
        next_pos = cur_pos[1], self.size - 1
        next_dir = 0, -1
        return self.right, next_pos, next_dir

    def overflow_up(self, cur_pos):
        next_pos = cur_pos[0], self.size - 1
        next_dir = 0, -1
        return self.up, next_pos, next_dir

    def overflow_down(self, cur_pos):
        next_pos = cur_pos[0], 0
        next_dir = 0, 1
        return self.down, next_pos, next_dir


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
