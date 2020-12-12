import re

from aoc.common.day_solver import DaySolver

INPUT_REGEX = re.compile(r'([A-Z])(\d+)')

DIRECTION_OFFSETS = {
    'N': (0, 1),
    'S': (0, -1),
    'W': (-1, 0),
    'E': (1, 0),
}
LEFT_TURN_DIRECTION = ['N', 'W', 'S', 'E']
RIGHT_TURN_DIRECTION = ['N', 'E', 'S', 'W']
TURN_DIRECTIONS = ['L', 'R']

LEFT_TURN_OFFSET = {
    0: lambda p: (p[0], p[1]),
    1: lambda p: (-p[1], p[0]),
    2: lambda p: (-p[0], -p[1]),
    3: lambda p: (p[1], -p[0]),
}
RIGHT_TURN_OFFSET = {
    0: lambda p: (p[0], p[1]),
    1: lambda p: (p[1], -p[0]),
    2: lambda p: (-p[0], -p[1]),
    3: lambda p: (-p[1], p[0]),
}


class Day12Solver(DaySolver):
    year = 2020
    day = 12

    def solve_puzzles(self):
        lines = self.load_all_input_lines()

        directions = []
        for line in lines:
            result = INPUT_REGEX.match(line)
            cmd = result.group(1)
            num = int(result.group(2))
            if cmd in TURN_DIRECTIONS:
                num = num // 90
            directions.append((cmd, num))

        x, y = self._part_1(directions, (0, 0), 'E')
        ans_one = abs(x) + abs(y)

        x, y = self._part_2(directions, (0, 0), (10, 1))
        ans_two = abs(x) + abs(y)
        return ans_one, ans_two

    def _part_1(self, directions, start_pos, start_dir):
        cur_pos = start_pos
        cur_dir = start_dir

        for cmd, num in directions:
            if cmd in DIRECTION_OFFSETS:
                cur_pos = self._advance_position(cur_pos, DIRECTION_OFFSETS[cmd], num)
            elif cmd == 'F':
                cur_pos = self._advance_position(cur_pos, DIRECTION_OFFSETS[cur_dir], num)
            elif cmd in TURN_DIRECTIONS:
                turns = LEFT_TURN_DIRECTION if cmd == 'L' else RIGHT_TURN_DIRECTION
                cur_dir = turns[(turns.index(cur_dir) + num) % 4]

        return cur_pos

    def _part_2(self, directions, start_pos, waypoint_start_pos):
        ship_pos = start_pos
        waypoint = waypoint_start_pos

        for cmd, num in directions:
            if cmd in DIRECTION_OFFSETS:
                waypoint = self._advance_position(waypoint, DIRECTION_OFFSETS[cmd], num)
            elif cmd == 'F':
                ship_pos = self._advance_position(ship_pos, waypoint, num)
            elif cmd in TURN_DIRECTIONS:
                offsets = LEFT_TURN_OFFSET if cmd == 'L' else RIGHT_TURN_OFFSET
                waypoint = offsets[num](waypoint)

        return ship_pos

    def _advance_position(self, start_pos, offset, num):
        return start_pos[0] + (offset[0] * num), start_pos[1] + (offset[1] * num)
