from collections import deque

from aoc.common.day_solver import DaySolver
from aoc.dec2019.common.intcode_processor import IntcodeProcessor


DIRECTIONS = {
    '^': (0, -1),
    'v': (0, 1),
    '>': (1, 0),
    '<': (-1, 0),
}

UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4


# Part 2 Notes
#   A   L 12 L 10 R  8 L 12
#   B   R  8 R 10 R 12
#   A   L 12 L 10 R  8 L 12
#   B   R  8 R 10 R 12
#   C   L 10 R 12 R  8
#   C   L 10 R 12 R  8
#   B   R  8 R 10 R 12
#   A   L 12 L 10 R  8 L 12
#   B   R  8 R 10 R 12
#   C   L 10 R 12 R  8


class Day17Solver(DaySolver):
    year = 2019
    day = 17

    def solve_puzzles(self):
        line = self.load_only_input_line()

        processor = IntcodeProcessor(program_str=line)
        layout = self._load_layout()
        vents, bot = self._find_vents_and_bot(layout)
        intersections = self._find_intersections(vents)

        ans_one = sum(a * b for a, b in intersections)

        processor.reset()
        processor.program[0] = 2

        # Manually Calculated
        main_routine = 'A,B,A,B,C,C,B,A,B,C'
        patterns = {
            'A': 'L,12,L,10,R,8,L,12',
            'B': 'R,8,R,10,R,12',
            'C': 'L,10,R,12,R,8',
        }
        expected_path = []
        for p in main_routine.split(','):
            expected_path.extend(patterns[p].split(','))
        path = self._find_path(vents, bot)
        assert expected_path == path

        input_queue = deque()
        self._add_to_queue(input_queue, main_routine)
        self._add_to_queue(input_queue, patterns['A'])
        self._add_to_queue(input_queue, patterns['B'])
        self._add_to_queue(input_queue, patterns['C'])
        self._add_to_queue(input_queue, 'n')

        processor.input_func = lambda: input_queue.popleft()
        processor.run_to_completion()
        ans_two = processor.last_output

        return ans_one, ans_two

    def _load_layout(self, processor=None):
        if not processor:
            return self.load_all_input_lines('17-p1')

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
            if self._next_pos(vent, offset) not in vents:
                return False
        return True

    def _find_path(self, vents, bot):
        cur_pos = bot[0]
        cur_dir = DIRECTIONS.get(bot[1])

        path = []
        while True:
            # Advance to next corner/intersection
            cur_pos, distance = self._advance_forward(vents, cur_pos, cur_dir)
            if distance:
                path.append(str(distance))

            # Try to turn left
            left_dir = cur_dir[1], -cur_dir[0]
            left_pos = self._try_turn(vents, cur_pos, left_dir)
            if left_pos:
                path.append('L')
                cur_dir = left_dir
                continue

            # Try to turn right
            right_dir = -cur_dir[1], cur_dir[0]
            right_pos = self._try_turn(vents, cur_pos, right_dir)
            if right_pos:
                path.append('R')
                cur_dir = right_dir
                continue

            return path

    def _advance_forward(self, vents, start_pos, cur_dir):
        cur_pos = start_pos
        moves = 0

        while True:
            next_pos = self._next_pos(cur_pos, cur_dir)
            if next_pos not in vents:
                return cur_pos, moves
            cur_pos = next_pos
            moves += 1

    def _try_turn(self, vents, cur_pos, next_dir):
        next_pos = self._next_pos(cur_pos, next_dir)
        return next_pos if next_pos in vents else None

    def _next_pos(self, cur_pos, direction):
        return cur_pos[0] + direction[0], cur_pos[1] + direction[1]

    def _add_to_queue(self, queue, values):
        for v in values:
            queue.append(ord(v))
        queue.append(10)
