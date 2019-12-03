from aoc.common.day_solver import DaySolver


class Day03Solver(DaySolver):
    year = 2019
    day = 3

    class WireMovement(object):
        def __init__(self, moves):
            self.cur_distance = 0
            self.cur_pos = (0, 0)
            self.visited_pos = dict()

            for move in moves:
                self._do_move(move)

        def _do_move(self, move):
            direction = move[0]
            distance = int(move[1:])

            if direction == 'U':
                slope = (0, 1)
            elif direction == 'D':
                slope = (0, -1)
            elif direction == 'L':
                slope = (-1, 0)
            elif direction == 'R':
                slope = (1, 0)
            else:
                raise Exception('Unknown Direction: ' + direction)

            for i in range(distance):
                self.cur_pos = self.cur_pos[0] + slope[0], self.cur_pos[1] + slope[1]
                self.cur_distance += 1

                if self.cur_pos not in self.visited_pos:
                    self.visited_pos[self.cur_pos] = self.cur_distance

    def solve_puzzles(self):
        lines = self._load_all_input_lines()

        wire_one = self.WireMovement(lines[0].split(','))
        wire_two = self.WireMovement(lines[1].split(','))

        intersections = [k for k in wire_one.visited_pos.keys() if k in wire_two.visited_pos]

        min_distance = None
        min_steps = None
        for pos in intersections:
            dist = abs(pos[0]) + abs(pos[1])
            if not min_distance or dist < min_distance:
                min_distance = dist

            steps = wire_one.visited_pos[pos] + wire_two.visited_pos[pos]
            if not min_steps or steps < min_steps:
                min_steps = steps

        return min_distance, min_steps
