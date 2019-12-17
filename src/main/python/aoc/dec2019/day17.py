import math
import re
from collections import deque
from itertools import islice, cycle

from aoc.common.day_solver import DaySolver
from aoc.common.dijkstra_search import DijkstraSearch
from aoc.dec2019.common.intcode_processor import IntcodeProcessor

ALL_NUMBERS_REGEX = re.compile(r'-?\d+')

DIRECTIONS = {
    '^': (0, 1),
    'v': (0, -1),
    '>': (1, 0),
    '<': (-1, 0),
}


class Day17Solver(DaySolver):
    year = 2019
    day = 17

    def solve_puzzles(self):
        line = self._load_only_input_line()

        processor = IntcodeProcessor(program_str=line)
        # layout = self._load_layout(processor)
        layout = self._load_layout()
        vents, bot = self._find_vents_and_bot(layout)
        intersections = self._find_intersections(vents)

        ans_one = sum(a * b for a, b in intersections)

        processor.reset()
        processor.program[0] = 2

        path = self._find_path(vents, bot)

        return ans_one, None

    def _load_layout(self, processor=None):
        if not processor:
            return self._load_all_input_lines('17-processed')

        layout = ''
        while True:
            val = processor.get_next_output()
            if processor.last_opcode == 99:
                break
            layout += chr(val)
        return layout.split('\n')

    def _find_vents_and_bot(self, layout):
        vents = set()
        bot = None
        for y, row in enumerate(layout):
            for x, val in enumerate(row):
                pos = (x, y)
                if val != '.':
                    vents.add(pos)

                if val in ['^', 'v', '<', '>']:
                    bot = pos, val
        return vents, bot

    def _find_intersections(self, vents):
        intersections = set()
        for v in vents:
            if self._is_intersection(vents, v):
                intersections.add(v)
        return intersections

    def _is_intersection(self, vents, vent):
        for offset in DIRECTIONS.values():
            pos = vent[0] + offset[0], vent[1] + offset[1]
            if pos not in vents:
                return False
        return True

    def _find_path(self, vents, bot):
        cur_pos = bot[0]
        direction = DIRECTIONS.get(bot[1])

        cur_moves = 0
        path = []
        visited = set()
        while True:
            visited.add(cur_pos)

            # Try to move first
            next_pos = self._next_pos(cur_pos, direction)
            if next_pos in vents:
                cur_moves += 1
                cur_pos = next_pos
                continue

            # Then attempt to turn left
            left_direction = -direction[1], -direction[0]
            left_pos = self._next_pos(cur_pos, left_direction)
            if left_pos not in visited and left_pos in vents:
                if cur_moves > 0:
                    path.append(cur_moves)
                    cur_moves = 0
                path.append('L')
                direction = left_direction
                continue

            # Then attempt to turn right
            right_direction = direction[1], direction[0]
            right_pos = self._next_pos(cur_pos, right_direction)
            if right_pos not in visited and right_pos in vents:
                if cur_moves > 0:
                    path.append(cur_moves)
                    cur_moves = 0
                path.append('R')
                direction = right_direction
                continue

            if cur_moves > 0:
                path.append(cur_moves)

            return path

    def _next_pos(self, cur_pos, direction):
        return cur_pos[0] + direction[0], cur_pos[1] + direction[1]

# L 12
# L 10
# L 8
# L 12
# L 8
# R 10
# L 12
# L 12
# R 10
# R 8
# R 12
# R 8
# L 10
# R 12
# R 10
# R 12
# L 8
# L 10
# L 12
# R 8
# L 8
# R 10
# L 12
# L 12
# R 10
# R 8
# R 12
# R 8
# L 10
# R 12
# R 10
# R 12
# L 8
