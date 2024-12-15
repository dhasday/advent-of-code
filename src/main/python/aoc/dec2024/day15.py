from collections import deque

from aoc.common import helpers
from aoc.common.day_solver import DaySolver


INST_TO_OFFSET = {
    '^': (0, -1),
    'v': (0, 1),
    '<': (-1, 0),
    '>': (1, 0),
}

ROBOT = '@'
BOX = 'O'
BOX_LEFT = '['
BOX_RIGHT = ']'
WALL = '#'


class Day15Solver(DaySolver):
    year = 2024
    day = 15

    def solve_puzzle_one(self):
        lines = self.load_all_input_lines()

        area_map = dict()
        robot_pos = None
        for y, line in enumerate(lines[:lines.index('')]):
            for x, val in enumerate(line):
                if val == ROBOT:
                    robot_pos = (x, y)
                elif val in [BOX, WALL]:
                    area_map[(x, y)] = val
        instructions = ''.join(lines[lines.index('') + 1:])

        for instruction in instructions:
            offset = INST_TO_OFFSET[instruction]
            next_pos = helpers.apply_deltas(robot_pos, offset)

            last_pos = next_pos
            last_val = area_map.get(next_pos)
            while last_val == BOX:
                last_pos = helpers.apply_deltas(last_pos, offset)
                last_val = area_map.get(last_pos)

            if last_val is None:
                robot_pos = next_pos
                next_val = area_map.pop(next_pos, None)
                if next_val == BOX:
                    area_map[last_pos] = BOX

        return self._get_coordinate_total(area_map, BOX)

    def solve_puzzle_two(self):
        lines = self.load_all_input_lines()

        area_map = dict()
        robot_pos = None
        for y, line in enumerate(lines[:lines.index('')]):
            for x, val in enumerate(line):
                if val == ROBOT:
                    robot_pos = (x * 2, y)
                elif val == BOX:
                    area_map[x * 2, y] = BOX_LEFT
                    area_map[x * 2 + 1, y] = BOX_RIGHT
                elif val == WALL:
                    area_map[x * 2, y] = WALL
                    area_map[x * 2 + 1, y] = WALL
                elif val in [BOX, WALL]:
                    area_map[(x, y)] = val
        instructions = ''.join(lines[lines.index('') + 1:])

        for instruction in instructions:
            offset = INST_TO_OFFSET[instruction]
            next_robot_pos = helpers.apply_deltas(robot_pos, offset)

            if next_robot_pos not in area_map:
                robot_pos = next_robot_pos
                continue

            to_move = deque()
            can_move = True
            if instruction in ['<', '>']:
                last_pos = next_robot_pos
                last_val = area_map.get(next_robot_pos)
                while last_val in [BOX_LEFT, BOX_RIGHT]:
                    to_move.append(last_pos)
                    last_pos = helpers.apply_deltas(last_pos, offset)
                    last_val = area_map.get(last_pos)
                can_move = last_val is None
            else:  # instruction in ['^', 'v']
                seen = set()
                to_check = deque()
                to_check.append(next_robot_pos)
                while to_check:
                    cur_pos = to_check.popleft()
                    if cur_pos in seen:
                        continue
                    seen.add(cur_pos)
                    cur_val = area_map.get(cur_pos)

                    if cur_val == WALL:
                        can_move = False
                        break
                    elif cur_val == BOX_LEFT:
                        to_move.append(cur_pos)
                        other_half = cur_pos[0] + 1, cur_pos[1]
                        to_move.append(other_half)

                        to_check.append(helpers.apply_deltas(cur_pos, offset))
                        to_check.append(helpers.apply_deltas(other_half, offset))
                    elif cur_val == BOX_RIGHT:
                        to_move.append(cur_pos)
                        other_half = cur_pos[0] - 1, cur_pos[1]
                        to_move.append(other_half)

                        to_check.append(helpers.apply_deltas(other_half, offset))
                        to_check.append(helpers.apply_deltas(cur_pos, offset))

            if can_move:
                while to_move:
                    cur_pos = to_move.pop()
                    next_pos = helpers.apply_deltas(cur_pos, offset)
                    if cur_pos in area_map:
                        val = area_map.pop(cur_pos)
                        area_map[next_pos] = val
                robot_pos = next_robot_pos

        return self._get_coordinate_total(area_map, BOX_LEFT)

    def _get_coordinate_total(self, area_map, box_char):
        coordinate_total = 0
        for (x, y), val in area_map.items():
            if val == box_char:
                coordinate_total += x + y * 100

        return coordinate_total

Day15Solver().print_results()